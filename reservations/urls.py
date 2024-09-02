from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('create/', views.create_reservation, name='create_reservation'), # fungerar
    path('list/', views.list_reservations, name='list_reservations'), # fungerar
=======
    path('create/', views.create_reservation, name='create_reservation'),
    path('list/', views.list_reservations, name='list_reservations'),
>>>>>>> ca15c55da2de11eab6d8730c8ff35acc20851b73
    path('update/<int:pk>/', views.update_reservation, name='update_reservation'),
    path('admin/bookings/', views.list_reservations, name='booking_management'), # fungerar
    path('success/<int:pk>/', views.success_reservation, name='success_reservation'), 
]