from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from django.forms import ModelForm

from .models import *


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangePhotoForm(ModelForm):
    photo = forms.ImageField(label='Фото', required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'type': 'file', 'accept': 'image/*'}))

    class Meta:
        model = CustomUser
        fields = ('photo',)


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваша почта'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))

    class Meta:
        model = CustomUser