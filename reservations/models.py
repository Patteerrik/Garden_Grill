from django.db import models
# Import Django's models module

class Reservation(models.Model):
    # Define a date field for the reservation date
    date = models.DateField()
    # Define a time field for the reservation time
    time = models.TimeField()
    # Define an integer field for the number of guests
    number_of_guests = models.IntegerField(default=1)
    # Define a char field to store the name for the reservation
    reservation_name = models.CharField(max_length=100)
    # Define an email field to store the user's email
    email = models.EmailField()

     # String representation of the reservation
    def __str__(self):
        return f"{self.reservation_name} - {self.date} at {self.time}"
