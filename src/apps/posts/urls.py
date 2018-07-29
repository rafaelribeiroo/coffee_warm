from django.urls import path
from .views import (
    post_list,
)

app_name = 'posts'
urlpatterns = [
    path('posts/', post_list, name='homepage'),
]
