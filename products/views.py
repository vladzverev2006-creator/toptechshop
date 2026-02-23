from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Product


def product_list(request):
    products = Product.objects.select_related('category', 'creator').order_by('-created_at')
    return render(request, 'products/product_list.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related('category', 'creator'), slug=slug)
    return render(request, 'products/product_detail.html', {'product': product})


def user_can_manage(user):
    if not user.is_authenticated:
        return False
    if user.is_staff:
        return True
    return user.groups.filter(name='seller').exists()


@login_required
def product_create(request):
    if not user_can_manage(request.user):
        return render(request, 'errors/403.html', status=403)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.creator = request.user
            product.save()
            form.save_m2m()
            messages.success(request, 'Товар создан')
            return redirect('products:detail', slug=product.slug)
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Создать товар'})


@login_required
def product_update(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if not (request.user == product.creator or user_can_manage(request.user)):
        return render(request, 'errors/403.html', status=403)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар обновлён')
            return redirect('products:detail', slug=product.slug)
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Редактировать товар'})


@login_required
def product_delete(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if not (request.user == product.creator or user_can_manage(request.user)):
        return render(request, 'errors/403.html', status=403)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Товар удалён')
        return redirect('products:index')
    return render(request, 'products/product_confirm_delete.html', {'product': product})
