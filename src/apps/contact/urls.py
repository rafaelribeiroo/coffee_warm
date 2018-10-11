from django.urls import path
from .views import (
    contato,
)

app_name = 'contact'
urlpatterns = [
    path('contato/', contato, name='fale_conosco'),
]
