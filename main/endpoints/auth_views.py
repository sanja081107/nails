from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView

from main.forms import *
from main.models import *


def user_logout(request):
    logout(request)
    return redirect('home')


class UserLogin(LoginView):
    form_class = LoginUserForm
    template_name = 'main/authorization.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        c_def = {
            'title': 'Авторизация',
            'block_title': 'Авторизация',
        }
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class UserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    slug_url_kwarg = 'slug'
    template_name = 'main/user_detail.html'
    context_object_name = 'el'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Данные пользователя'
        context['block_title'] = 'Данные пользователя'
        return context
