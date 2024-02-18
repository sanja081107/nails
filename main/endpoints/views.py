import datetime

from allauth.account.models import EmailAddress
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from main.forms import *
from main.models import *


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')


class HomeView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['title'] = 'Главная'
        return context


class ManicureView(TemplateView):
    template_name = 'main/manicure.html'

    def get_context_data(self, **kwargs):
        context = super(ManicureView, self).get_context_data(**kwargs)
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        all_posts = Manicure.objects.filter(date__gt=yesterday, client=None, is_active=True)            # поиск всех свободных дней

        free_dates = []
        for el in all_posts:
            free_dates.append(str(el.date))
        free_dates.append(str(today))

        if not self.request.user.is_authenticated:                                                      # Если пользователь не авторизован
            dates = free_dates
        else:                                                                                           # Если пользователь авторизован
            n = 1                                                                                       # сколько дней за и после неактивны со дня записи
            busy_posts = Manicure.objects.filter(date__gt=yesterday, client=self.request.user)          # поиск всех предстоящих записей для пользователя

            busy_dates = []
            if busy_posts:
                for el in busy_posts:
                    for i in range(n+1):
                        busy_dates.append(str(el.date - datetime.timedelta(days=i)))
                        busy_dates.append(str(el.date + datetime.timedelta(days=i)))
            dates = set(free_dates) - set(busy_dates)
            dates = list(dates)

        context['title'] = 'Запись на маникюр'
        context['body_title'] = 'Запись на маникюр'
        context['dates'] = dates
        return context


def times_result(request):
    today = datetime.datetime.today()
    if request.method == 'GET':
        date_str = request.GET.get('datepicker_value')
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        if date < today:
            date = None
            return render(request, 'main/times_result.html', context={'date': date})
    if not date:
        date = today
    times = Manicure.objects.filter(date=date, client=None, is_active=True)
    context = {
        'times': times,
        'date': date,
    }
    return render(request, 'main/times_result.html', context)


def times_admin_result(request):
    if request.user.is_staff:
        if request.method == 'GET':
            date_str = request.GET.get('admin_datepicker_value')
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        if not date:
            date = datetime.date.today()

        context = {'date': date}

        return render(request, 'main/times_result.html', context)
    else:
        return HttpResponse("Ошибка доступа")


class SelectServiceView(LoginRequiredMixin, TemplateView):
    template_name = 'main/select_service.html'
    login_url = reverse_lazy('user_login')

    def get_context_data(self, **kwargs):
        context = super(SelectServiceView, self).get_context_data(**kwargs)
        post = Manicure.objects.get(pk=self.kwargs['pk'])

        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)

        all_posts = Manicure.objects.filter(date__gt=yesterday, client=None, is_active=True)        # поиск всех свободных дней
        free_dates = []
        for el in all_posts:
            free_dates.append(str(el.date))
        free_dates.append(str(today))

        n = 1                                                                                       # сколько дней за и после неактивны со дня записи
        busy_posts = Manicure.objects.filter(date__gt=yesterday, client=self.request.user)          # поиск всех предстоящих записей для пользователя
        busy_dates = []
        if busy_posts:
            for el in busy_posts:
                for i in range(n+1):
                    busy_dates.append(str(el.date - datetime.timedelta(days=i)))
                    busy_dates.append(str(el.date + datetime.timedelta(days=i)))
        dates = set(free_dates) - set(busy_dates)
        dates = list(dates)

        if str(post.date) in dates:
            context['title'] = 'Выберите услугу'
            context['body_title'] = 'Выберите услугу'
            context['form'] = ServiceForm(initial={'service': post.service})
            context['pk'] = self.kwargs['pk']
        else:
            context['error'] = 'Ошибка'
        return context


def confirm_manicure(request, pk):
    post = Manicure.objects.get(pk=pk)

    post.client = request.user
    post.service = Service.objects.get(id=request.POST['service'])
    post.is_active = False
    post.save()
    return redirect('user_history', slug=request.user.slug)


class EditManicureView(UpdateView):
    template_name = 'main/edit_manicure.html'
    pk_url_kwarg = 'pk'
    model = Manicure
    form_class = ManicureForm
    success_url = reverse_lazy('manicure')

    def get_context_data(self, **kwargs):
        context = super(EditManicureView, self).get_context_data(**kwargs)
        return context


def delete_manicure(request, pk):
    post = Manicure.objects.get(pk=pk)
    if (request.user.is_authenticated and request.user == post.client) or request.user.is_staff:
        post.is_active = True
        post.service = None
        post.client = None
        post.save()

    return redirect('user_history', slug=request.user.slug)


class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['title'] = 'О нас'
        context['body_title'] = 'О нас'
        return context


class ContactsView(TemplateView):
    template_name = 'main/contacts.html'

    def get_context_data(self, **kwargs):
        context = super(ContactsView, self).get_context_data(**kwargs)
        context['title'] = 'Контакты'
        context['body_title'] = 'Контакты'
        return context
