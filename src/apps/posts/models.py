from django.db import models

# Salvar as imgs com tec UUID, para evitar conflito de nomes.
import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible
# Fim imports UUID

# Imports reading time estimate
from django.utils.safestring import mark_safe
# Lembrar de provisionar o pacote com:
# pip install django-markdown-deux
# Incluir markdown_deux nas installed_apps
from markdown_deux import markdown

from django.dispatch import receiver
from django.db.models.signals import pre_save
# Fim reading_time

# Import slugify para o front-end
# from django.utils.text import slugify
# Fim slugify

# Import datetime
import datetime  # Atributo created
from django.utils import timezone

# Import auth
from django.conf import settings


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
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        super(Tag, self).save(*args, **kwargs)


class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=1,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
    )
    title = models.CharField('Título', max_length=120)
    # slug = models.SlugField(unique=True, max_length=250)
    image = models.ImageField(
        'Imagem',
        upload_to=RandomFileName('imgs_uploaded'),
        null=True,
        blank=True,
        width_field="width_field",
        height_field="height_field",
    )
    width_field = models.IntegerField('Largura da imagem', default=0)
    height_field = models.IntegerField('Altura', default=0)
    # iframe_youtube = models.CharField('Link do Youtube', max_length=50)
    content = models.TextField('Conteúdo')
    # Sempre draft, a menos que você indique o contrário
    draft = models.BooleanField('Rascunho', default=True)
    read_time = models.CharField(max_length=20, null=True, blank=True)
    tag = models.ManyToManyField(Tag, related_name='blog', blank=True)
    created = models.DateField('Publicação', default=datetime.date.today)
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
        return self.title  # return self.slug + " " + str(self.created)

    class Meta:
        ordering = ['title']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    # Retira todas as tags que você tiver passado no content
    # para ir limpo pro template
    def get_markdown(self):
        content = self.content
        return mark_safe(markdown(content))

    # Função para "slugar" o título no django admin
    '''def save(self, *args, **kwargs):
        self.slug = slugify(self.title+str(self.created))
        super(Post, self).save(*args, **kwargs)'''

    # Função para "slugifar" o front-end
    # def get_absolute_url(self):
    # return reverse("posts:detail", kwargs={"slug": self.slug})


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
        elif content_length > 240:
            instance.read_time = 'menos que 1 minuto'
# Fim da função

# Método slugify para o front-end, falta o do admin


'''def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug'''

pre_save.connect(CountReadTime, sender=Post)
