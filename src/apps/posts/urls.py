from django.urls import path, re_path
from .views import (
    post_list,
    post_create,
    tag_create,
    PostDetailView,
    post_by_tag,
    # post_update,
)

app_name = 'posts'
urlpatterns = [
    path('posts/', post_list, name='homepage'),
    path('posts/redigir/', post_create, name='post_create'),
    re_path(r'^post/(?P<slug>[\w-]+)/$', PostDetailView.as_view(), name='detail'),
    path('criar/tag', tag_create, name='tag_create'),
    re_path(r'^tag=(?P<tag>[\w-]+)/$', post_by_tag, name='post_by_tag'),
    # re_path(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'), Colocar no postdetailview, personalBlog
]
