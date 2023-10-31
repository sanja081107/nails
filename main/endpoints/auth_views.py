from allauth.account.views import LoginView, SignupView
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from main.forms import *
from main.models import *


def user_logout(request):
    logout(request)
    return redirect('home')


class UserLogin(LoginView):

    def get_context_data(self, **kwargs):
        cont = super(UserLogin, self).get_context_data(**kwargs)
        ret = {
            'title': 'Авторизация',
            'body_title': 'Авторизация',
        }
        context = dict(list(cont.items()) + list(ret.items()))
        return context


class UserRegister(SignupView):

    def get_context_data(self, **kwargs):
        ret = super(UserRegister, self).get_context_data(**kwargs)
        ret.update(
            {
                'title': 'Регистрация',
                'body_title': 'Регистрация',
            }
        )
        return ret


class UserDetailView(DetailView, UpdateView):
    model = CustomUser
    slug_url_kwarg = 'slug'
    template_name = 'main/user_detail.html'
    context_object_name = 'el'

    form_class = CustomUserChangePhotoForm

    login_url = reverse_lazy('user_login')

    def get_success_url(self):
        user = CustomUser.objects.get(slug=self.kwargs['slug'])
        return user.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Данные пользователя'
        context['body_title'] = 'Данные пользователя'
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    slug_url_kwarg = 'slug'
    template_name = 'main/user_update.html'
    form_class = CustomUserChangeForm

    def get_success_url(self):
        user = CustomUser.objects.get(slug=self.kwargs['slug'])
        return user.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение данных'
        context['body_title'] = 'Изменение данных'
        if self.request.user.slug == self.kwargs['slug']:
            return context
        else:
            context['error'] = 'Ошибка доступа'
            return context
