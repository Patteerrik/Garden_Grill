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
    elif 'cancel' in request.POST:
        reservation.delete()
        return redirect('list_reservations')

    return render(request, 'reservations/update_reservation.html', {'form': form, 'reservation': reservation})
    
def create_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            new_reservation = form.save()
            return redirect('success_reservation', pk=new_reservation.pk)
        else:
            print(form.errors)
    else:
        form = ReservationForm()

    return render(request, 'reservations/create_reservation.html', {'form': form})

<<<<<<< HEAD
def success_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(request, 'reservations/success_reservation.html', {'reservation': reservation})

def list_reservations(request):
    reservations = Reservation.objects.all()
    return render(request, 'reservations/list_reservation.html')


=======
def list_reservations(request):
    reservations = Reservation.object.all()
    return render(request, 'reservations/list_reservations.html', {'reservations': reservations})

def booking_management(request):
    return render(request, 'reservations/booking_management.html')
>>>>>>> ca15c55da2de11eab6d8730c8ff35acc20851b73

