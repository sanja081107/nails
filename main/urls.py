from django.urls import path
from main.endpoints.views import *
from main.endpoints.auth_views import *
from main.endpoints.pass_views import *

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contacts/', contacts, name='contacts'),

    path('password_change/', PasswordChange.as_view(), name='password_change'),
    path('password_change_done/', PasswordChangeDone.as_view(), name='password_change_done'),
    path('password_reset/', PasswordReset.as_view(), name='password_reset'),
    path('password_reset_done/', PasswordResetDone.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<slug:uidb64>/<slug:token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetComplete.as_view(), name='password_reset_complete'),

    path('account/login/', UserLogin.as_view(), name='user_login'),
    path('account/signup/', UserRegister.as_view(), name='user_register'),
    path('user_detail/<slug:slug>/', UserDetailView.as_view(), name='user_detail'),
    path('user_update/<slug:slug>/', UserUpdateView.as_view(), name='user_update'),
    path('user_logout/', user_logout, name='user_logout'),
]
