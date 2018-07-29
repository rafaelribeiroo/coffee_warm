from django.urls import path, re_path
from .views import (
    post_list,
    post_create,
    PostDetailView,
)

app_name = 'posts'
urlpatterns = [
    path('', post_list, name='homepage'),
    path('redigir/', post_create, name='post_create'),
    re_path(r'^(?P<slug>[\w-]+)/$', PostDetailView.as_view(), name='detail'),
]
