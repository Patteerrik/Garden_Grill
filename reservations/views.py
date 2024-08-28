from django.http import HttpResponse
from .models import Reservation

def create_reservation(request):
    return HttpResponse("Reservation created!")

def list_reservations(request):
    reservations = Reservation.objects.all()
    # if there is no reservations
    if not reservations:
        return HttpResponse("No reservations found.")
    # else show reservations
    reservations_list = '\n'.join([f"{res.reservation_name} - {res.date} at {res.time}" for res in reservations])
    return HttpResponse(reservations_list)
    
    ########UPPDATERA##########