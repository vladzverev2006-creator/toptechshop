from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='index'),
    path('create/', views.product_create, name='create'),
    path('<slug:slug>/', views.product_detail, name='detail'),
    path('<slug:slug>/edit/', views.product_update, name='edit'),
    path('<slug:slug>/delete/', views.product_delete, name='delete'),
]
