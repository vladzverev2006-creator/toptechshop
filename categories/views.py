from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoryForm
from .models import Category


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories/category_list.html', {'categories': categories})


def user_can_manage(user):
    return user.is_authenticated and (user.is_staff or user.groups.filter(name='seller').exists())


@login_required
def category_create(request):
    if not user_can_manage(request.user):
        return HttpResponseForbidden('Недостаточно прав')
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория создана')
            return redirect('categories:index')
    else:
        form = CategoryForm()
    return render(request, 'categories/category_form.html', {'form': form, 'title': 'Создать категорию'})


@login_required
def category_update(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if not user_can_manage(request.user):
        return HttpResponseForbidden('Недостаточно прав')
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория обновлена')
            return redirect('categories:index')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'categories/category_form.html', {'form': form, 'title': 'Редактировать категорию'})


@login_required
def category_delete(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if not user_can_manage(request.user):
        return HttpResponseForbidden('Недостаточно прав')
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Категория удалена')
        return redirect('categories:index')
    return render(request, 'categories/category_confirm_delete.html', {'category': category})
