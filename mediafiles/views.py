from django.shortcuts import render

# Create your views here.


def placeholder(request):
    from django.http import HttpResponse
    return HttpResponse('Placeholder for app')
