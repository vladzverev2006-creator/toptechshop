from django.urls import path
from . import views

app_name = 'mediafiles'

urlpatterns = [
    path('', views.placeholder, name='index'),
]
