from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render
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
        context['title'] = 'Запись на маникюр'
        context['body_title'] = 'Запись на маникюр'
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
