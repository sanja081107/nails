from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from django.forms import ModelForm

from .models import *


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2")


class CustomUserChangeForm(UserChangeForm):

    email = forms.CharField(label='Электронная почта', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Почта'}))
    photo = forms.ImageField(label='Фото', required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'type': 'file', 'accept': 'image/*'}))
    instagram = forms.CharField(label='Инстаграм', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Инстаграм'}))
    mobile = forms.CharField(label='Мобильный телефон', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'tel', 'id': 'tel', 'maxlength': '18', 'placeholder': 'Телефон'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'photo', 'instagram', 'mobile')


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
