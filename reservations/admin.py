from django.contrib import admin
# Import the admin module from Django
from .models import Reservation
# Import the Reservation model

# Register your models here.
admin.site.register(Reservation)
# Registers the Reservation model with the Django admin site,
# so it can be managed in the admin interface.
