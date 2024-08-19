from django.db import models

# Create your models here.
class Reservation(models.Model):
    date = models.DateField()
    time = models.TimeField()
    number_of_guest = models.IntegerField()
    reservation_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.reservation_name} - {self.date} at {self.time}"