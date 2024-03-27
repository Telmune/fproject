from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.urls import path, reverse_lazy

from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.register_user, name='register'),

    ]