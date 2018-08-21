from django.urls import path, re_path
from .views import (
    search_titles,
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
    path('buscar/', search_titles, name='buscar'),
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
