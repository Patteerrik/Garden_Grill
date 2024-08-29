from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Reservation
from .forms import ReservationForm

def is_admin_user(user):
    return user.is_authenticated and user.is_superuser

@login_required
@user_passes_test(is_admin_user)

def update_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    form = ReservationForm(request.POST or None, instance=reservation)

    if 'update' in request.POST and form.is_valid():
        form.save()
        return redirect('list_reservations')
    elif 'cnacel' in request.POST:
        reservation.delete()
        return redirect('list_reservations')

    return render(request, 'reservations/update_reservation.html', {'form': form, 'reservation': reservation})
    
def create_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            new_reservation = form.save()
            return redirect('reservation_detail', pk=new_reseravtion.pk)
    else:
        form = ReservationForm()
    return render(request, 'reservations/create_reservation.html', {'form': form})

def booking_management(request):
    return render(request, 'reservations/booking_management.html')

