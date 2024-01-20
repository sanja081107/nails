import datetime

from allauth.account.models import EmailAddress
from django.contrib.auth import logout
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
        # if self.request.user.is_authenticated:
        #     try:
        #         post = EmailAddress.objects.get(email=self.request.user.email)
        #         if post and post.verified:
        #             context['verify'] = 'verified'
        #         else:
        #             logout(self.request)
        #             context['verify'] = 'not verified'
        #     except:
        #         return context
        return context

class ManicureView(TemplateView):
    template_name = 'main/manicure.html'

    def get_context_data(self, **kwargs):
        context = super(ManicureView, self).get_context_data(**kwargs)

        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        posts = Manicure.objects.filter(date__gt=yesterday, client=None, is_active=True)

        dates = []
        for el in posts:
            dates.append(str(el.date))
        dates.append(str(today))

        context['title'] = 'Запись на маникюр'
        context['body_title'] = 'Запись на маникюр'
        context['today'] = today
        context['dates'] = dates
        return context


def search_times(request):
    if request.method == 'GET':
        date = request.GET.get('datepicker_value')
    if not date:
        date = datetime.date.today()
    times = Manicure.objects.filter(date=date, client=None, is_active=True)
    context = {'times': times}
    return render(request, 'main/times_result.html', context)


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
