from django.contrib import admin
from django.urls import path, include

# Multiple URLs
from src.apps.core import urls as core_urls
from src.apps.posts import urls as posts_urls

# ImageField
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # CMS django
    path('admin/', admin.site.urls),
    # Qntos views resenha teve
    path('hitcount/', include('hitcount.urls')),
    # Editor WYSIWYG
    path('froala_editor/', include('froala_editor.urls')),
    path('', include((core_urls), namespace='utils')),
    path('', include((posts_urls), namespace='post')),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
