from django.urls import path, re_path
from .views import (
    post_list,
    post_create,
    post_update,
    PostDetailView,
    tag_create,
    post_by_tag,
)

app_name = 'posts'
urlpatterns = [
    path('posts/', post_list, name='homepage'),
    path('posts/redigir/', post_create, name='post_create'),
    re_path(r'^post/(?P<slug>[\w-]+)/$', PostDetailView.as_view(), name='detail'),
    re_path(r'^post/(?P<slug>[\w-]+)/editar/$', post_update, name='update'),
    path('criar/tag/', tag_create, name='tag_create'),
    re_path(r'^post/tag=(?P<tag_slug>[\w-]+)/$', post_by_tag, name='post_by_tag'),
    # re_path(r'^post/tag=(?P<tag>[\w-]+)/$', post_by_tag, name='post_by_tag'),
]
