from django.db import models


class Reservation(models.Model):
    date = models.DateField()
    time = models.TimeField()
    number_of_guests = models.IntegerField(default=1)
    reservation_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.reservation_name} - {self.date} at {self.time}"
