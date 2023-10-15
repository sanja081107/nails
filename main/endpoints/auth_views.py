from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, CreateView, TemplateView

from main.forms import *
from main.models import *


def user_logout(request):
    logout(request)
    return redirect('home')


class UserLogin(LoginView):
    form_class = LoginUserForm
    template_name = 'main/user_login.html'

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


class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'main/user_register.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        c_def = {
            'title': 'Регистрация',
            'block_title': 'Регистрация',
        }
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class UserDetailView(LoginRequiredMixin, DetailView, UpdateView):
    model = CustomUser
    slug_url_kwarg = 'slug'
    template_name = 'main/user_detail.html'
    context_object_name = 'el'

    form_class = CustomUserChangePhotoForm

    login_url = reverse_lazy('authorization')

    def get_success_url(self):
        user = CustomUser.objects.get(slug=self.kwargs['slug'])
        return user.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Данные пользователя'
        context['block_title'] = 'Данные пользователя'
        return context
