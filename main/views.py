from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render

from .models import *


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')


def home(request):
    context = {
        'title': 'Главная страница'
    }
    return render(request, 'main/index.html', context)


def about(request):
    return HttpResponse("About page")


def contacts(request):
    return HttpResponse("Contacts page")


def authorization(request):
    return HttpResponse("Authorization page")


def user_detail(request, slug):
    email = CustomUser.objects.get(slug=slug).email
    return HttpResponse(f"User detail page {email}")
