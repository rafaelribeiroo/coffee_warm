from django.db import models

# Salvar as imgs com tec UUID, para evitar conflito de nomes.
import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible
# Fim imports UUID

# Imports reading time estimate
from django.utils.safestring import mark_safe
from markdown_deux import markdown

from django.dispatch import receiver
from django.db.models.signals import pre_save
# Fim reading_time

# Import slugify para o front-end
from django.utils.text import slugify
from django.urls import reverse
# Fim slugify

# Import datetime
import datetime  # Atributo created
from django.utils import timezone

# Import auth
from django.conf import settings

# Unique slug
from .utils import unique_slug_generator

# Tag
from .unique_slug import generate_unique_slug

# Notify subscriber
from django.core.mail import send_mass_mail
from src import settings

from .unsubscribe_link import generate_unsubscribe_link
from django.utils.safestring import mark_safe

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


# Métodos para armazenar as imagens com UUID name
@deconstructible
class RandomFileName(object):
    def __init__(self, path):
        self.path = os.path.join(path, "%s%s")

    def __call__(self, _, filename):
        extension = os.path.splitext(filename)[1]
        return self.path % (uuid4(), extension)
# Fim método


# Classe para lidar com draft e post
class PostQuerySet(models.query.QuerySet):
    def not_draft(self):
        return self.filter(draft=False)

    def published(self):
        return self.filter(publish__lte=timezone.now()).not_draft()


class PostManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return PostQuerySet(self.model, using=self._db)

    def active(self, *args, **kwargs):
        return self.get_queryset().published()
# Fim classe draft


class Tag(models.Model):
    title = models.CharField('Titulo', max_length=50)
    slug = models.SlugField('URL do Titulo', max_length=100, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post:post_by_tag', args=[self.slug])  # homepage

    def save(self, *args, **kwargs):
        self.title = self.title.upper()
        if self.slug:  # edit
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(Tag, self.title)
        else:  # create
            self.slug = generate_unique_slug(Tag, self.title)
        # self.slug = slugify(self.title)
        # Pega o titulo e cria um slug, so nao assegura que o slug seja unico, diferente do Post
        super(Tag, self).save(*args, **kwargs)


class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=1,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
    )
    title = models.CharField('Título', max_length=120)
    slug = models.SlugField('URL do titulo', unique=True, max_length=250)
    tag = models.ManyToManyField(
        Tag,
        related_name='blog',
        verbose_name='Tag correspondente'
    )
    image = models.ImageField(
        'Imagem',
        upload_to=RandomFileName('imgs_uploaded'),
        blank=False,
        width_field="width_field",
        height_field="height_field",
    )
    width_field = models.IntegerField('Largura da imagem', default=0)
    height_field = models.IntegerField('Altura', default=0)
    iframe_youtube = models.CharField(
        'Link do Youtube',
        max_length=50,
        default="ala/ii22"
    )
    content = models.TextField('Conteúdo')
    # Sempre draft, a menos que você indique o contrário
    draft = models.BooleanField('Rascunho', default=True)
    read_time = models.CharField(
        'Tempo de leitura',
        max_length=20,
        null=True,
        blank=True
    )
    publish = models.DateField('Publicação', default=datetime.date.today)
    updated = models.DateTimeField(
        'Alteração',
        auto_now=True,
        auto_now_add=False)
    timestamp = models.DateTimeField(
        'Tempo recorrente',
        auto_now=False,
        auto_now_add=True)

    # Lidando com o draft e post
    objects = PostManager()

    def __str__(self):
        return self.title  # return self.title

    class Meta:
        ordering = ['-timestamp', '-updated']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    # Retira todas as tags que você tiver passado no content
    # para ir limpo pro template
    def get_markdown(self):
        content = self.content
        return mark_safe(markdown(content))

    # Função para "slugifar" o front-end
    def get_absolute_url(self):
        return reverse("post:detail", kwargs={"slug": self.slug})  # Criar o detalhe antes

    def save(self, *args, **kwargs):
        # slug = slugify(self.title)
        # if self.slug != slug:
        #    self.slug = slug
        if self.draft is False:
            self.notify_subscribers()
        return super(Post, self).save(*args, **kwargs)

    def notify_subscribers(self):
        subject = "Novo post em 'Catarse Literária' sobre: " + self.title
        from_email = settings.DEFAULT_FROM_EMAIL
        link_to_review = settings.DOMAIN_POSTS + self.slug
        for recipient in Subscriber.objects.all():
            context = {
                'person': recipient.first_name,
                'title': self.title,
                'unsubscribe': generate_unsubscribe_link(
                    recipient.email_address
                ),
                'link': link_to_review,
            }
            recipes = [recipient.email_address]
            html_content = render_to_string('mail.html', context)
            msg = EmailMultiAlternatives(
                subject,
                html_content,
                from_email,
                to=recipes,
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()


    """def notify_subscribers(self):
                    subject = "Novo post em: 'Catarse Literária' sobre: " + self.title

                    emails = tuple(
                        (subject,
                         Post.create_subscriber_notification_email(subscriber),
                         # "Rafael Ribeiro <pereiraribeirorafael@gmail.com>",
                         settings.DEFAULT_FROM_EMAIL,
                         [subscriber.email_address])
                        for subscriber in Subscriber.objects.all())

                    send_mass_mail(emails)

                @staticmethod
                def create_subscriber_notification_email(subscriber):
                    message_content = "Check out Catarse newest insights at " + settings.DOMAIN + reverse('post:homepage') + " !"
                    # message_content = "Check out Catarse newest insights at 127.0.0.1"
                    footer = "Se você gostaria de se desinscrever, vá até o devido link: "\
                             + generate_unsubscribe_link(subscriber.email_address)
                    message = "Caro {name},\r\n{message_content}\r\n\r\n{footer}".format(name=subscriber.first_name,
                                                                                         # Var acima, mensagem a ser enviada
                                                                                         message_content=message_content,
                                                                                         # Ultima var
                                                                                         footer=footer)
                    return message"""


class Subscriber(models.Model):
    first_name = models.CharField('Primeiro nome', max_length=200)
    email_address = models.EmailField('Endereco de e-mail', unique=True)

    def __str__(self):
        return self.first_name


# Função para estimar o tempo de leitura aproximadamente
@receiver(pre_save, sender=Post)
def CountReadTime(sender, instance, **kwargs):
    if instance is not None:
        content_length = len(instance.content)
        if content_length > 240:
            minutes = content_length // 240
            if minutes > 15:
                minutes = 15
            if minutes == 1:
                instance.read_time = '~1 minuto'
            else:
                instance.read_time = '~' + str(minutes) + ' minutos'
        elif content_length < 240:
            instance.read_time = 'menos que 1 minuto'
# Fim da função


def create_slug(instance, new_slug=None):
    # Método slugify para o front-end
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(CountReadTime, sender=Post)
pre_save.connect(pre_save_post_receiver, sender=Post)
