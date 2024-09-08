
from django.urls import path, include
from . import views # Imports the views module



urlpatterns = [
    path('', views.home, name='home'),
    path('hello/', views.hello, name='hello'),
    path('bookings/', views.bookings, name='bookings'),
    path('menu/', views.menu, name='menu'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
]