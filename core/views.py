from django.shortcuts import render


def home(request):
    return render(request, 'core/home.html')


def error_404(request, exception):
    return render(request, 'errors/404.html', status=404)


def error_500(request):
    return render(request, 'errors/500.html', status=500)


def test_500(request):
    raise Exception('Test 500 error')
