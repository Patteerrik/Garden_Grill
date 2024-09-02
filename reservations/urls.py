from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_reservation, name='create_reservation'), # fungerar
    path('list/', views.list_reservations, name='list_reservations'), # fungerar
    path('update/<int:pk>/', views.update_reservation, name='update_reservation'),
    path('admin/bookings/', views.list_reservations, name='booking_management'), # fungerar
    path('success/<int:pk>/', views.success_reservation, name='success_reservation'), 
]