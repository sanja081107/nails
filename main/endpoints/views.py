import datetime

from allauth.account.models import EmailAddress
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

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

        if not self.request.user.is_authenticated:
            yesterday = today - datetime.timedelta(days=1)
            posts = Manicure.objects.filter(date__gt=yesterday, client=None, is_active=True)

            dates = []
            for el in posts:
                dates.append(str(el.date))
            dates.append(str(today))
        else:
            n = 1                                                                                       # сколько дней за и после неактивны со дня записи
            yesterday = today - datetime.timedelta(days=1)
            all_dates = Manicure.objects.filter(date__gt=yesterday, client=None, is_active=True)        # поиск всех свободных дней
            busy_dates = Manicure.objects.filter(date__gt=yesterday, client=self.request.user)          # поиск всех предстоящих записей для пользователя

            all_dates_list = []
            for el in all_dates:
                all_dates_list.append(str(el.date))
            all_dates_list.append(str(today))

            busy_dates_list = []
            if busy_dates:
                for el in busy_dates:
                    for i in range(n+1):
                        busy_dates_list.append(str(el.date - datetime.timedelta(days=i)))
                        busy_dates_list.append(str(el.date + datetime.timedelta(days=i)))
            dates = set(all_dates_list) - set(busy_dates_list)
            dates = list(dates)

        context['title'] = 'Запись на маникюр'
        context['body_title'] = 'Запись на маникюр'
        context['dates'] = dates
        return context


def search_times(request):
    if request.method == 'GET':
        date_str = request.GET.get('datepicker_value')
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    if not date:
        date = datetime.date.today()
    times = Manicure.objects.filter(date=date, client=None, is_active=True)
    context = {
        'times': times,
        'date': date,
    }
    return render(request, 'main/times_result.html', context)


class SelectServiceView(LoginRequiredMixin, TemplateView):
    template_name = 'main/select_service.html'
    login_url = reverse_lazy('user_login')

    def get_context_data(self, **kwargs):
        context = super(SelectServiceView, self).get_context_data(**kwargs)
        context['time'] = self.kwargs['pk']
        return context


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
