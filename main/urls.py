from django.urls import path
from main.endpoints.views import *
from main.endpoints.auth_views import *

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contacts/', contacts, name='contacts'),

    path('authorization/', UserLogin.as_view(), name='authorization'),
    path('user_logout/', user_logout, name='user_logout'),
    path('user_detail/<slug:slug>/', UserDetailView.as_view(), name='user_detail'),
]
