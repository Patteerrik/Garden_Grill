from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_reservation, name='create_reservation'),
    # path('list/', views.list_reservations, name='list_reservations'),
    path('update/<int:pk>/', views.update_reservation, name='update_reservation'),
    # path('cancel/<int:pk>/', views.cancel_reservation, name='cancel_reservation'),
    path('admin/bookings/', views.booking_management, name='booking_management')

]