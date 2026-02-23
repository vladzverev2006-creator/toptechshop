import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from categories.models import Category
from products.models import Product
from reviews.models import Review


def error_response(code, message, status=400):
    return JsonResponse({'error': {'code': code, 'message': message}}, status=status)


def serialize_product(product):
    return {
        'id': product.id,
        'title': product.title,
        'slug': product.slug,
        'price': str(product.price),
        'category': product.category.name,
        'rating': float(product.rating_avg),
    }


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def products_list(request):
    qs = Product.objects.select_related('category').all()
    search = request.GET.get('search')
    category = request.GET.get('category')
    order = request.GET.get('order')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if search:
        qs = qs.filter(title__icontains=search)
    if category:
        qs = qs.filter(category__slug=category)
    if min_price:
        qs = qs.filter(price__gte=min_price)
    if max_price:
        qs = qs.filter(price__lte=max_price)
    if order == 'price_asc':
        qs = qs.order_by('price')
    elif order == 'price_desc':
        qs = qs.order_by('-price')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return error_response('forbidden', 'Требуется авторизация', 403)
        body = json.loads(request.body.decode('utf-8') or '{}')
        try:
            category_obj = Category.objects.get(slug=body.get('category'))
        except Category.DoesNotExist:
            return error_response('invalid_category', 'Категория не найдена', 400)
        product = Product.objects.create(
            title=body.get('title', 'Новый товар'),
            description=body.get('description', ''),
            price=body.get('price', 0),
            status='active',
            creator=request.user,
            category=category_obj,
            license_id=body.get('license_id') or 1,
        )
        return JsonResponse(serialize_product(product), status=201)

    limit = int(request.GET.get('limit', 10))
    offset = int(request.GET.get('offset', 0))
    data = [serialize_product(p) for p in qs[offset:offset + limit]]
    return JsonResponse({'results': data, 'count': qs.count()})


@csrf_exempt
@require_http_methods(['GET', 'POST', 'PUT', 'DELETE'])
def product_detail(request, pk):
    try:
        product = Product.objects.select_related('category').get(pk=pk)
    except Product.DoesNotExist:
        return error_response('not_found', 'Товар не найден', 404)

    if request.method == 'GET':
        return JsonResponse(serialize_product(product))

    if not request.user.is_authenticated:
        return error_response('forbidden', 'Требуется авторизация', 403)

    if request.method == 'DELETE':
        product.delete()
        return JsonResponse({'status': 'deleted'})

    body = json.loads(request.body.decode('utf-8') or '{}')
    if request.method == 'POST':
        return error_response('method_not_allowed', 'Используйте /api/products/ для POST', 405)

    if request.method == 'PUT':
        product.title = body.get('title', product.title)
        product.price = body.get('price', product.price)
        product.save()
        return JsonResponse(serialize_product(product))


@require_http_methods(['GET'])
def categories_list(request):
    data = [{'id': c.id, 'name': c.name, 'slug': c.slug} for c in Category.objects.all()]
    return JsonResponse({'results': data})


@require_http_methods(['GET'])
def reviews_list(request):
    data = [{'product': r.product.title, 'rating': r.rating, 'comment': r.comment} for r in Review.objects.all()]
    return JsonResponse({'results': data})


@require_http_methods(['GET'])
@login_required
def my_orders(request):
    data = [{'id': o.id, 'status': o.status, 'total': str(o.total)} for o in request.user.orders.all()]
    return JsonResponse({'results': data})


def api_docs(request):
    return render(request, 'api/docs.html')
