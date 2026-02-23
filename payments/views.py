from django.shortcuts import render


def payment_success(request):
    return render(request, 'payments/success.html')


def payment_failed(request):
    return render(request, 'payments/failed.html')
