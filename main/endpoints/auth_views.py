from allauth.account.views import LoginView, SignupView
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, CreateView

from main.forms import *
from main.models import *


def user_logout(request):
    logout(request)
    return redirect('home')


class UserLogin(LoginView):

    def get_context_data(self, **kwargs):
        ret = super(UserLogin, self).get_context_data(**kwargs)
        ret.update(
            {
                'title': 'Авторизация',
                'body_title': 'Авторизация',
            }
        )
        return ret


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
        context['body_title'] = 'Данные пользователя'
        return context
