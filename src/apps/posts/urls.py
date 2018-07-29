from django.urls import path, re_path
from .views import (
    post_list,
    PostDetailView,
    post_create,
)

app_name = 'posts'
urlpatterns = [
    path('', post_list, name='homepage'),
    re_path(
        r'^(?P<slug>[\w-]+)view/$',
        PostDetailView.as_view(),
        name='detail'
    ),
    path('create/', post_create, name='post_create'),
]
