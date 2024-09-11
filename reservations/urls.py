from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'reservations'

urlpatterns = [
    path('create/', views.create_reservation, name='create_reservation'),
    path('list/', views.list_reservation, name='list_reservation'),
    #path('update/<int:pk>/', views.update_reservation, name='update_reservation'),
    #path('admin/bookings/', views.booking_management, name='booking_management'),
    path('reservations/success/<int:pk>/', views.success_reservation, name='success_reservation'),
    #path('reservations/edit<int:reservation_id>/', views.edit_reservation, name='edit_reservation'),
    path('logged_in_user/', views.logged_in_user, name='logged_in_user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logged_in_admin/', views.logged_in_admin, name='logged_in_admin'),
    path('change/', views.change_reservation, name='change_reservation'),
]