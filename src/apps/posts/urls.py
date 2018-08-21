from django.urls import path, re_path
from .views import (
    SearchSubmitView,
    SearchAjaxSubmitView,
    post_list,
    post_create,
    post_update,
    PostDetailView,
    tag_create,
    post_by_tag,
)

app_name = 'posts'
urlpatterns = [
    # Buscar titulos
    path('search_ajax/', SearchSubmitView.as_view(), name='search-submit'),
    # Response ajax busca
    path('search_submit/', SearchAjaxSubmitView.as_view(), name='search-ajax-submit'),
    # Listagem de resenhas
    path('posts/', post_list, name='homepage'),
    # Criacao
    path('posts/redigir/', post_create, name='post_create'),
    # Detalhes
    re_path(r'^post/(?P<slug>[\w-]+)/$', PostDetailView.as_view(), name='detail'),
    # Edicao
    re_path(r'^post/(?P<slug>[\w-]+)/editar/$', post_update, name='update'),
    # Criacao de tag
    path('criar/tag/', tag_create, name='tag_create'),
    # Resenhas por tag
    re_path(r'^post/tag=(?P<tag_slug>[\w-]+)/$', post_by_tag, name='post_by_tag'),
]
