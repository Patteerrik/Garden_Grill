from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Reservation
from .forms import ReservationForm
from django.contrib import messages # To show messages to the user
from django.conf import settings
from django.db.models import Sum # To summarize number of guests


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
    elif 'cancel' in request.POST:
        reservation.delete()
        return redirect('list_reservations')

    return render(request, 'reservations/update_reservation.html', {'form': form, 'reservation': reservation})
    
def create_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            number_of_guests = form.cleaned_data['number_of_guests']

            existing_reservations = Reservation.objects.filter(date=date, time=time).aggregate(Sum('number_of_guests'))
            booked_seats =  existing_reservations['number_of_guests__sum'] or 0

            if booked_seats + number_of_guests <= 50:
                new_reservation = form.save()
                return redirect('success_reservation', pk=new_reservation.pk)
            else:
                messages.error(request, f"Only {50 - booked_seats} seats are available for the selected time.")
        else:
            messages.error(request, f" There was an error in the form. Please try again")
    else:
        form = ReservationForm()

    return render(request, 'reservations/create_reservation.html', {'form': form})


def success_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(request, 'reservations/success_reservation.html', {'reservation': reservation})

def list_reservations(request):
    reservations = Reservation.objects.all()
    return render(request, 'reservations/list_reservations.html', {'reservations': reservations})

def booking_management(request):
    return render(request, 'reservations/booking_management.html')


