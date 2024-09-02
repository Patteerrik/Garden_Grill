from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
<<<<<<< HEAD
        fields = ['reservation_name', 'date', 'time', 'number_of_guests']
=======
        fields = ['reservation_name', 'date', 'time', 'number_of_guest']
>>>>>>> ca15c55da2de11eab6d8730c8ff35acc20851b73
