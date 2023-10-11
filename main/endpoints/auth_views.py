from django.http import HttpResponse
from django.shortcuts import render

from main.models import *


def authorization(request):
    context = {
        'block_title': 'Авторизация'
    }
    return render(request, 'main/authorization.html', context)


def user_detail(request, slug):
    email = CustomUser.objects.get(slug=slug).email
    return HttpResponse(f"User detail page {email}")
