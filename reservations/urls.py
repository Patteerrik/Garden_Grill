from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_reservation, name='create_reservation'),
    path('list/', views.list_reservations, name='list_reservations'),
]