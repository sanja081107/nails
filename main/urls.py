from django.urls import path
from main.endpoints.views import *
from main.endpoints.auth_views import *
from main.endpoints.pass_views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('manicure/', ManicureView.as_view(), name='manicure'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('about/', AboutView.as_view(), name='about'),

    path('times_result/', times_result, name='times_result'),
    path('select_service/<int:pk>/', SelectServiceView.as_view(), name='select_service'),
    path('confirm_manicure/<int:pk>/', confirm_manicure, name='confirm_manicure'),
    path('delete_manicure/<int:pk>/', delete_manicure, name='delete_manicure'),

    path('password_change/', PasswordChange.as_view(), name='password_change'),
    path('password_change_done/', PasswordChangeDone.as_view(), name='password_change_done'),
    path('password_reset/', PasswordReset.as_view(), name='password_reset'),
    path('password_reset_done/', PasswordResetDone.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<slug:uidb64>/<slug:token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetComplete.as_view(), name='password_reset_complete'),

    path('account/login/', UserLogin.as_view(), name='user_login'),
    path('account/signup/', UserRegister.as_view(), name='user_register'),
    path('user_detail/<slug:slug>/', UserDetailView.as_view(), name='user_detail'),
    path('user_history/<slug:slug>/', UserHistoryView.as_view(), name='user_history'),
    path('user_update/<slug:slug>/', UserUpdateView.as_view(), name='user_update'),
    path('user_logout/', user_logout, name='user_logout'),
]
