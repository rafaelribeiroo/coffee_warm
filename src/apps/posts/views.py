from django.shortcuts import (
    # Maioria das respostas dos métodos
    render,
    # Se não houver um objeto, apresenta 404
    get_object_or_404,
    # Após efetuar tal transação, redireciona a tal template
    redirect,
    # Lista de tag, ou 404
    get_list_or_404
)
# Importando as entidades do DB, referenciar
from .models import Post, Tag, Subscriber
# Importando os forms, trabalhar com DML
from .forms import PostForm, TagForm, SubscriberForm, UnsubscribeForm
# Com o decorador transaction.atomic, vai executar a transação no bd
# apenas se o método produzir uma resposta sem erros
from django.db import transaction
# Se um usuário anônimo tentar abrir a URL criar/post apresenta 404
# HttpResponseRedirect para tratar os "get_absolute_url"
from django.http import Http404, HttpResponseRedirect
# timezone, se a publicação do post for superior a data atual,
# será incluído em: "Posts futuros"
from django.utils import timezone
# Ele pega o conteúdo do atributo e substitui todos os
# caracteres especiais para o conteúdo ser mantido
from urllib.parse import quote_plus
# Mensagens nativas do django quando um evento ocorre
from django.contrib import messages


# Function Buscar
from django.views.generic.base import View
from django.http import HttpResponse
from django.template import loader

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .unsubscribe_link import generate_unsubscribe_link
from django.core.signing import Signer, BadSignature
import base64
from django.core.mail import send_mail


class SearchSubmitView(View):
    template = 'search_submit.html'
    response_message = 'Esta é a solicitação a resposta'

    def post(self, request, *args, **kwargs):
        template = loader.get_template(self.template)
        query = request.POST.get('search', '')

        # Uma simples query para os objetos Post que contém 'query'
        items = Post.objects.filter(title__icontains=query)

        context = {
            'title': self.response_message,
            'query': query,
            'items': items,
        }

        rendered_template = template.render(context, request)
        return HttpResponse(rendered_template, content_type='text/html')


class SearchAjaxSubmitView(SearchSubmitView):
    template = 'search_results.html'
    response_message = 'Essa é a resposta em AJAX, vindo direto do banco'


def post_list(request):
    # Se a publicação do post for amanhã, printa: "futuro post"
    today = timezone.now().date()
    num_posts = len(Post.objects.all())
    queryset_list = Post.objects.active()  # .order_by('-timestamp')
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()

    # A partir de 5 posts, inicia a paginação
    paginator = Paginator(queryset_list, 5)

    page = request.GET.get('page', 1)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)

    context = {
        'today': today,
        'posts': numbers,
        'num_posts': num_posts,
        # 'posts': queryset_list,
        # Paginação
    }
    return render(request, 'post_list.html', context)


@transaction.atomic
def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        # instance.user = request.user
        instance.save()
        form.save_m2m()
        # Message Success
        messages.success(request, "Criado com sucesso")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'form': form,
    }
    return render(request, 'post_create.html', context)


@transaction.atomic
def post_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        form.save_m2m()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "post_update.html", context)


from django.views.generic import DetailView


class PostDetailView(DetailView):
    template_name = 'post_detail.html'

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        instance = get_object_or_404(Post, slug=slug)
        if instance.publish > timezone.now().date() or instance.draft:
            if not self.request.user.is_staff or not self.request.user.is_superuser:
                raise Http404
        return instance

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        instance = context['object']
        context['share_string'] = quote_plus(instance.content)
        return context


def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect('post:homepage')


@transaction.atomic
def tag_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = TagForm(request.POST or None)
    context = {
        'form': form,
    }
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return redirect('utils:homepage')  # Return reverse url
    return render(request, 'tag_create.html', context)


def post_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    queryset = get_list_or_404(Post, tag=tag)
    context = {
        'tag': tag,
        'posts': queryset,
    }
    return render(request, 'post_by_tag.html', context)


def subscribe(request):
    """Renderiza um formulario que habilita os leitores a se inscreverem"""
    if request.method == "POST":
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "subscribe_success.html", request.POST, status=201)
        else:
            return render(request, "subscribe.html", {"subscribe_form":form})
    else:
        subscribe_form = SubscriberForm()
        return render(request, "subscribe.html", {"subscribe_form": subscribe_form})


def unsubscribe_request(request):
    """ Renderiza um formulario que permite os inscritos se desinscreverem """
    if request.method == "POST":
        form = UnsubscribeForm(request.POST)
        error_message = ""
        status = 400
        if form.is_valid():
            subscriber_email = form.cleaned_data["email_address"]
            try:
                Subscriber.objects.get(email_address=subscriber_email)
                unsubscribe_link = generate_unsubscribe_link(subscriber_email)
                unsubscribe_email_message = "Favor, navegue ate o seguinte link para se desinscrever:\r\n" + unsubscribe_link
                send_mail("Link para se desinscrever", unsubscribe_email_message, "Catarse Literaria <enquantoesquentaocafe@gmail.com>",
                          recipient_list=[subscriber_email])
                message = "Um email foi enviado para " + subscriber_email + " contendo o link para se desinscrever do meu blog."
                return render(request, "unsubscribe_result.html", {"message": message})
            except Subscriber.DoesNotExist:
                error_message = "Desculpe, o email informado nao foi encontrado em nossa lista de inscritos."
                status = 404

        # else if form is not valid, return with error messages
        return render(request, "unsubscribe_request.html",
                      {"unsubscribe_form": form, "error_message": error_message}, status=status)
    else:
        form = UnsubscribeForm()
        return render(request, "unsubscribe_request.html", {"unsubscribe_form": form})


def blog_unsubscribe(request, unsubscribe_token):
    """ Desinscreve um inscrito se a requisicao conter um token valido"""
    status = 200
    padded_token = unsubscribe_token + ("=" * (4 - len(unsubscribe_token) % 4))
    token_bytes = padded_token.encode("UTF-8")
    decoded = base64.b64decode(token_bytes)
    signer = Signer(salt="unsubscribe")
    subscriber_email = ""
    try:
        subscriber_email = signer.unsign(decoded.decode("UTF-8"))
        Subscriber.objects.get(email_address=subscriber_email).delete()
        message = subscriber_email + " foi desinscrito com sucesso."
    except Subscriber.DoesNotExist:
        message = subscriber_email + " ja estava desinscrito. Nenhuma acao foi tomada."
        status = 404
    except BadSignature:
        message = "Nos desculpe, porem esta URL nao foi reconhecida."
        status = 404
    except UnicodeDecodeError:
        message = "Nos desculpe, porem esta URL nao foi reconhecida."
        status = 404
    return render(request, "unsubscribe_result.html", {"message": message}, status=status)
