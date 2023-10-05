from django.http import HttpResponseNotFound
from django.shortcuts import render


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')


def home(request):
    context = {
        'title': 'Главная страница'
    }
    return render(request, 'main/index.html', context)

