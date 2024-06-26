import datetime

from allauth.account.models import EmailAddress
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView

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


class AddManicureView(CreateView):
    form_class = ManicureForm
    template_name = 'main/edit_manicure.html'
    success_url = reverse_lazy('manicure')

    def form_valid(self, form):
        day = str(form.cleaned_data.get('date'))
        day = day.split('-')
        time_out = str(form.cleaned_data.get('time'))
        time_out = time_out.split(':')
        form.instance.title = day[2] + '.' + day[1] + '.' + day[0][2:] + ' ' + str(form.cleaned_data.get('time')) + '-' + str(int(time_out[0])+2) + ':' + time_out[1]
        try:
            return super().form_valid(form)
        except:
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AddManicureView, self).get_context_data(**kwargs)
        context['form'] = ManicureForm(initial={'date': self.kwargs['date']})
        return context


class DeleteManicureView(DeleteView):
    model = Manicure
    pk_url_kwarg = 'pk'
    context_object_name = 'el'
    success_url = reverse_lazy('manicure')
    template_name = 'main/manicure_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super(DeleteManicureView, self).get_context_data(**kwargs)
        context['title'] = 'Удаление записи'
        context['body_title'] = 'Подтвердите удаление'
        return context


def times_result(request):
    today = datetime.datetime.today().date()
    if request.method == 'GET':
        date_str = request.GET.get('datepicker_value')
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        if date < today:
            date = None
            return render(request, 'main/times_result.html', context={'date': date})

    times = Manicure.objects.filter(date=date, client=None, is_active=True)
    context = {
        'times': times,
        'date': date,
    }
    return render(request, 'main/times_result.html', context)


def times_result_admin(request):
    today = datetime.datetime.today().date()
    if request.method == 'GET':
        date_str = request.GET.get('datepicker_value_admin')
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        if date < today:
            date = None
            return render(request, 'main/times_result.html', context={'date': date})

    times = Manicure.objects.filter(date=date, client=None, is_active=True)
    context = {
        'times': times,
        'date': date,
    }
    return render(request, 'main/times_result_admin.html', context)


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
    post.service = Service.objects.get(pk=request.POST['service'])
    post.is_active = False
    post.save()
    return redirect('user_history', slug=request.user.slug)


class EditServiceView(LoginRequiredMixin, UpdateView):
    template_name = 'main/edit_manicure.html'
    pk_url_kwarg = 'pk'
    model = Manicure
    form_class = ServiceForm

    login_url = reverse_lazy('user_login')

    def get_success_url(self):
        return reverse('user_history', kwargs={'slug': self.request.user.slug})

    def get_context_data(self, **kwargs):
        context = super(EditServiceView, self).get_context_data(**kwargs)
        post = Manicure.objects.get(pk=self.kwargs['pk'])

        if post.client == self.request.user and post.date >= datetime.date.today():
            context['title'] = 'Выберите услугу'
            context['body_title'] = 'Выберите услугу'
        else:
            context['error'] = 'Ошибка'
        return context


class EditManicureView(LoginRequiredMixin, UpdateView):
    template_name = 'main/edit_manicure.html'
    pk_url_kwarg = 'pk'
    model = Manicure
    form_class = ManicureForm
    success_url = reverse_lazy('manicure')

    login_url = reverse_lazy('user_login')

    def get_context_data(self, **kwargs):
        context = super(EditManicureView, self).get_context_data(**kwargs)
        if self.request.user.is_staff:
            context['title'] = 'Изменить данные'
            context['body_title'] = 'Изменить данные'
        else:
            context['error'] = 'Ошибка'
        return context


def cancel_manicure(request, pk):
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
