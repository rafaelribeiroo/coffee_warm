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
from .models import Post, Tag
# Importando os forms, trabalhar com DML
from .forms import PostForm, TagForm
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
    return render(request, 'post_form.html', context)


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
    return render(request, 'post_form.html', context)


def post_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    queryset = get_list_or_404(Post, tag=tag)
    context = {
        'tag': tag,
        'posts': queryset,
    }
    return render(request, 'post_by_tag.html', context)
