from django.urls import path
from .views import (
    SearchSubmitView,
    SearchAjaxSubmitView,
    post_list,
    post_create,
    post_update,
    post_detail,
    post_delete,
    tag_create,
    post_by_tag,
    subscribe,
    unsubscribe_request,
    blog_unsubscribe,
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
    path('post/<slug>/', post_detail, name='detail'),
    # Edicao
    path('post/<slug>/editar/', post_update, name='update'),
    # Exclusao
    path('<slug>/excluir/', post_delete, name='delete'),
    # Criacao de tag
    path('criar/tag/', tag_create, name='tag_create'),
    # Resenhas por tag
    path('post/tag=<slug:tag_slug>/', post_by_tag, name='post_by_tag'),
    # Inscrever para receber notificacoes
    path('subscribe/', subscribe, name='blog_subscribe'),
    # Pagina de requisicao de unsubscribe
    path('unsubscribe/', unsubscribe_request, name='unsubscribe_request'),
    # Unsubscribe com sucesso
    path('unsubscribe/<str:unsubscribe_token>', blog_unsubscribe, name='unsubscribe'),
]
