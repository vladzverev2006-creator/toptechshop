from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.category_list, name='index'),
    path('create/', views.category_create, name='create'),
    path('<slug:slug>/edit/', views.category_update, name='edit'),
    path('<slug:slug>/delete/', views.category_delete, name='delete'),
]
