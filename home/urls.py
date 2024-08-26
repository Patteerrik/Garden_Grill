
from django.urls import path
from . import views # Imports the views module


urlpatterns = [
    path('', views.home, name='home'),
    path('hello/', views.hello, name='hello'),
    path('bookings/', views.bookings, name='bookings'),
    path('menu/', views.menu, name='menu'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
]