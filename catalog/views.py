from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from categories.models import Category
from products.models import Product


def catalog_list(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    ordering = request.GET.get('order', 'new')

    products = Product.objects.select_related('category', 'creator').prefetch_related('tags')

    if query:
        products = products.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category:
        products = products.filter(category__slug=category)

    if ordering == 'price_asc':
        products = products.order_by('price')
    elif ordering == 'price_desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created_at')

    paginator = Paginator(products, 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    categories = Category.objects.all()
    return render(request, 'catalog/catalog_list.html', {'page_obj': page_obj, 'query': query, 'categories': categories})
