from django.db import models

# Create your models here.
class Reservation(models.Model):
    date = models.DateField()
    time = models.TimeField()
    number_of_guest = models.IntegerField()
    reservation_name = models.CharField(max_length=100)