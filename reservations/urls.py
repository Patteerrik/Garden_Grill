from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_reservation, name='create_reservation'),
    # path('list/', views.list_reservations, name='list_reservations'),
    path('update/<int:pk>/', views.update_reservation, name='update_reservation'),
    path('admin/bookings/', views.booking_management, name='booking_management'),
    path('success/<int:pk>/', views.success_reservation, name='success_reservation'),
    path('reservations/', views.list_reservations, name='list_reservations'),
    path('reservations/edit<int:reservation_id>/', views.edit_reservation, name='edit_reservation'),
]