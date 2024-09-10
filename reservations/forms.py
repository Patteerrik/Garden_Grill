from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['reservation_name', 'date', 'time', 'number_of_guests']  
