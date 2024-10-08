from django.urls import path
# Import the path function to define URL patterns
from . import views
# Import views from the current app reservations
from django.contrib.auth.views import LogoutView
# Import Django's built-in LogoutView to handle user logouts


app_name = 'reservations'

# Define URL patterns for the reservations app
urlpatterns = [
    path('create/',
         views.create_reservation, name='create_reservation'),
    path('list/',
         views.list_reservation, name='list_reservation'),
    path('reservations/success/<int:pk>/',
         views.success_reservation, name='success_reservation'),
    path('success_email/', views.success_email, name='success_email'),
    path('logged_in_user/',
         views.logged_in_user, name='logged_in_user'),
    path('logout/',
         LogoutView.as_view(), name='logout'),
    path('logged_in_admin/',
         views.logged_in_admin, name='logged_in_admin'),
    path('change/',
         views.change_reservation, name='change_reservation'),
    path('edit/<int:reservation_id>/',
         views.edit_reservation, name='edit_reservation'),
    path('my-reservations/',
         views.users_reservations, name='users_reservations'),
]
