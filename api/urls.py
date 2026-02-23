from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.api_docs, name='index'),
    path('products/', views.products_list, name='products_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('categories/', views.categories_list, name='categories_list'),
    path('reviews/', views.reviews_list, name='reviews_list'),
    path('orders/', views.my_orders, name='my_orders'),
]
