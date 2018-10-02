from django.urls import path
from .views import (
    HomePageView,
)

app_name = 'utils'
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
]
