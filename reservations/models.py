from django.db import models

# Create your models here.
class Reservation(models.Model):
    date = models.DateField()
    time = models.TimeField()
<<<<<<< HEAD
    number_of_guests = models.IntegerField(default=1)
=======
    number_of_guest = models.IntegerField(default=1)
>>>>>>> ca15c55da2de11eab6d8730c8ff35acc20851b73
    reservation_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.reservation_name} - {self.date} at {self.time}"