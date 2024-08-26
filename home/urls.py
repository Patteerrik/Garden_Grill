
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hello/', views.hello, name='hello'),
    path('bookings/', views.bookings, name='bookings'),
    path('menu/', views.menu, name='menu'),
]