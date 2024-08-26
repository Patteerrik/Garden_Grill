
from django.urls import path
from . import views, hello, bookings, menu, register

urlpatterns = [
    path('', views.home, name='home'),
    path('hello/', views.hello, name='hello'),
    path('bookings/', views.bookings, name='bookings'),
    path('menu/', views.menu, name='menu'),
    path('register/', register, name='register'),
]