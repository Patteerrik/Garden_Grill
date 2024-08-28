from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Booking(models.Model):
    # Link each booking to a user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    # Stores the booking´s date and time
    booking_date = models.DateTimeField()
    # Booking status options
    status = models.CharField(max_length=10, choices=[('confirmed', 'Confirmed'), ('pending', 'Pending'), ('cancelled', 'Cancelled')])
    # Number of guest for the booking
    number_of_guests = models.IntegerField()
    # Returns a more readable string
    def __str__(self):
        return f"{self.user.username} - {self.booking_date.strftime('%Y-%m-%d %H:%M')}"
