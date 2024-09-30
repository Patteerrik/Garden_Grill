from django import forms
from .models import Reservation
from datetime import time


# Define opening hours
OPENING_TIME = time(12, 0)  # 12:00 PM
CLOSING_TIME = time(22, 0)  # 10:00 PM

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['reservation_name', 'date', 'time', 'number_of_guests']  

    
    def clean_time(self):
        reservation_time = self.cleaned_data.get('time')

        # Check time is beetween 12:00 PM and 10:00 PM
        if not (OPENING_TIME <= reservation_time <= CLOSING_TIME):
            raise forms.ValidationError("The reservation time must be between 12:00 PM and 10:00 PM.")

        return reservation_time
