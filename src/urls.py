from django.contrib import admin
from django.urls import path, include

# Multiple URLs
from src.apps.core import urls as core_urls
from src.apps.posts import urls as posts_urls

# ImageField
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include((core_urls), namespace='core')),
    path('', include((posts_urls), namespace='post')),
]

if settings.DEBUG is True:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
