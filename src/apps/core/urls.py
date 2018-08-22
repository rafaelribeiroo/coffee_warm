from django.urls import path
from .views import (
    home,
)

app_name = 'utils'
urlpatterns = [
    path('', home, name='homepage'),
]
