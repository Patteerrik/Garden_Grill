from django.http import HttpResponse
from .models import Reservation

def create_reservation(request):
    return HttpResponse("Reservation created!")

def list_reservations(request):
    reservations = Reservation.objects.all()
    return HttpRespons(reservations)