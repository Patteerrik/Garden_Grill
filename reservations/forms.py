from django import forms
from .models import Reservation
from datetime import time, datetime, date
from django.contrib.auth import get_user_model
# Import of necessary modules for forms, datetime handling, and user model


# Define opening hours
OPENING_TIME = time(12, 0)  # 12:00 PM
CLOSING_TIME = time(22, 0)  # 10:00 PM


class ReservationForm(forms.ModelForm):
    # Email field for staff/admin users, not required for regular users
    email = forms.EmailField(required=False, label="Email for reservation")

    class Meta:
        # Use the Reservation model
        model = Reservation
        # Specify the fields that will be included in the form
        fields = ['reservation_name', 'date', 'time', 'number_of_guests']

    # Custom validation for the reservation date
    def clean_date(self):
        reservation_date = self.cleaned_data.get('date')
        today = date.today()

        # Check that the reservation date is not in the past
        if reservation_date < today:
            raise forms.ValidationError(
                "The reservation date cannot be in the past."
                )

        # Return the cleaned date if valid
        return reservation_date

    # Custom validation for the reservation time
    def clean_time(self):
        reservation_time = self.cleaned_data.get('time')
        reservation_date = self.cleaned_data.get('date')
        current_time = datetime.now().time()

        # Check time is beetween 12:00 PM and 10:00 PM
        if not (OPENING_TIME <= reservation_time <= CLOSING_TIME):
            raise forms.ValidationError(
                "The reservation time must be between 12:00 PM and 10:00 PM."
                )

        # Checks that time is not in the past
        if (
            reservation_date == date.today() and
            reservation_time < current_time
        ):
            raise forms.ValidationError(
                "The reservation time cannot be in the past."
            )

        # Return the cleaned time if valid
        return reservation_time

    # Custom validation for the email field
    def clean_email(self):
        email = self.cleaned_data.get('email')
        User = get_user_model()

        # Only validate email if it's provided
        if email:
            # Check if the email exists in the user database
            if not User.objects.filter(email=email).exists():
                raise forms.ValidationError(
                    "This email is not registered. "
                    "Please use a registered email."
                )

        # Return the email if valid
        return email
