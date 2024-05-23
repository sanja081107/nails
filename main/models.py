from django.contrib.auth.models import User, AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from slugify import slugify
from django.urls import reverse

from .managers import CustomUserManager


def upload_photo_autor(instance, filename):
    return 'photos/users/{0}/{1}'.format(instance.slug, filename)


class CustomUser(AbstractUser):

    email = models.EmailField(_("email address"), unique=True)

    slug = models.SlugField(verbose_name='Ваш ID', unique=True, db_index=True, null=True)
    photo = models.ImageField(upload_to=upload_photo_autor, verbose_name='Фото', null=True, blank=True)
    instagram = models.CharField(max_length=50, verbose_name='Инстаграм', null=True, blank=True)
    mobile = models.CharField(max_length=20, verbose_name='Телефон', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Зарегистрирован')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.email)
        self.username = self.email
        return super(CustomUser, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.email


class Manicure(models.Model):
    title = models.CharField(max_length=20, verbose_name='Название', blank=True, null=True, validators=[RegexValidator(regex=r'^([1-31].)', message='такое время существует')], unique=True)
    time = models.CharField(max_length=5, verbose_name='Время', validators=[RegexValidator(regex=r'^(([0,1][0-9])|(2[0-2])):(([0-5][0-9])|(00))$', message='Неверный формат времени!')])
    client = models.ForeignKey('CustomUser', on_delete=models.SET_DEFAULT, verbose_name='Клиент', default=None, blank=True, null=True)
    service = models.ForeignKey('Service', on_delete=models.DO_NOTHING, verbose_name='Доступные услуги', default=None, blank=True, null=True)
    date = models.DateField(verbose_name='Дата', default=None)
    is_active = models.BooleanField(verbose_name='Опубликовать', default=True)

    # def save(self, *args, **kwargs):
    #     day = str(self.date)
    #     day = day.split('-')
    #     time_out = str(self.time)
    #     time_out = time_out.split(':')
    #     self.title = day[2] + '.' + day[1] + '.' + day[0][2:] + ' ' + str(self.time) + '-' + str(int(time_out[0])+2) + ':' + time_out[1]        # 21.08.24 19:00-21:00
    #
    #     return super(Manicure, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи на ногти'
        ordering = ['-date', 'title']


class Service(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название', validators=[RegexValidator(regex=r'$', message='Неверный формат поля!')])
    price = models.IntegerField(default=0, verbose_name='Цена в рублях')

    def save(self, *args, **kwargs):
        self.title = str(self.title) + ' = ' + str(self.price) + 'р.'
        return super(Service, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Мои услуги'
        ordering = ['id']
