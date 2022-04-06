
from django.urls import path     
from . import views

urlpatterns = [
    path('',views.root),
    path('home',views.home_page),
    path('register',views.register),
    path('login',views.login),
    path('logout',views.logout),
]
