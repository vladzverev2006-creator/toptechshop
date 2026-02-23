from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('test500/', views.test_500, name='test_500'),
]
