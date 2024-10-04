from django import forms
from .models import Reservation
from datetime import time, datetime, date
from django.contrib.auth import get_user_model


# Define opening hours
OPENING_TIME = time(12, 0)  # 12:00 PM
CLOSING_TIME = time(22, 0)  # 10:00 PM

class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ['reservation_name', 'date', 'time', 'number_of_guests']  

    
    def clean_date(self):
        reservation_date = self.cleaned_data.get('date')
        today = date.today()
        
        if reservation_date < today:
            raise forms.ValidationError("The reservation date cannot be in the past.")

        return reservation_date
    
    def clean_time(self):
        reservation_time = self.cleaned_data.get('time')
        reservation_date = self.cleaned_data.get('date')
        current_time = datetime.now().time()

        # Check time is beetween 12:00 PM and 10:00 PM
        if not (OPENING_TIME <= reservation_time <= CLOSING_TIME):
            raise forms.ValidationError("The reservation time must be between 12:00 PM and 10:00 PM.")

        if reservation_date == date.today() and reservation_time < current_time:
            raise forms.ValidationError("The reservation time cannot be in the past.")


        return reservation_time

    # Non registrated emails cannot be used
    def clean_email(self):
        email = self.cleaned_data.get('email')
        User = get_user_model()

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is not registered. Please use a registered email.")
        
        return email
