from django.contrib import admin
from django.urls import path, include

# Multiple URLs
from src.apps.core import urls as core_urls
from src.apps.posts import urls as posts_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include((core_urls), namespace='core')),
    path('posts/', include((posts_urls), namespace='post')),
]
