from django.shortcuts import render


def favorites_list(request):
    return render(request, 'favorites/favorites_list.html')
