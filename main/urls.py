from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contacts/', contacts, name='contacts'),

    path('authorization/', authorization, name='authorization'),
    path('user_detail/<slug:slug>/', user_detail, name='user_detail'),
]
