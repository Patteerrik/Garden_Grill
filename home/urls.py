
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views # Imports the views module


urlpatterns = [
    path('', views.home, name='home'),
    path('hello/', views.hello, name='hello'),
    path('bookings/', views.bookings, name='bookings'),
    path('menu/', views.menu, name='menu'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='home/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
]