from django.contrib.auth.models import User, AbstractUser
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
    mobile = models.CharField(max_length=13, verbose_name='Телефон', null=True, blank=True)
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
