from django.shortcuts import render
from django.db.models import Count

from categories.models import Category


def about(request):
    return render(request, 'pages/about.html')


def contact(request):
    return render(request, 'pages/contact.html')


def faq(request):
    return render(request, 'pages/faq.html')


def stats(request):
    data = Category.objects.annotate(total=Count('products')).order_by('-total')
    return render(request, 'pages/stats.html', {'data': data})
