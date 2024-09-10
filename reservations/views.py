from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Reservation
from .forms import ReservationForm
from django.contrib import messages # To show messages to the user
from django.conf import settings
from django.db.models import Sum # To summarize number of guests
from django.core.mail import send_mail
from collections import defaultdict

def logged_in_user(request):
    # check if user is admin
    if request.user.is_staff:
        return render(request, 'reservations/logged_in_admin.html')
    else:
        # If user is not admin show user page
        return render(request, 'reservations/logged_in_user.html')


def is_admin_user(user):
    return user.is_staff


@login_required
def logged_in_admin(request):
    return render(request, 'reservations/logged_in_admin.html')


@login_required
@user_passes_test(is_admin_user) # Ev ta bort
def update_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    form = ReservationForm(request.POST or None, instance=reservation)

    if 'update' in request.POST and form.is_valid():
        form.save()
        return redirect('list_reservation')
    elif 'cancel' in request.POST:
        reservation.delete()
        return redirect('list_reservation')

    return render(request, 'reservations/update_reservation.html', {'form': form, 'reservation': reservation})


@login_required
@user_passes_test(is_admin_user)
def list_reservation(request):
    reservations = Reservation.objects.all()
    # Dictionary to store reserved seats by date and time
    spots_per_time = defaultdict(lambda: {'reserved_spots': 0, 'available_spots': 50})

    # Loop through all reservations an group by date and time
    for res in reservations:
        key = (res.date, res.time)
        spots_per_time[key]['reserved_spots'] += res.number_of_guests
        spots_per_time[key]['available_spots'] = 50 - spots_per_time[key]['reserved_spots']

    # Convert to a list to send to the template
    # https://www.w3schools.com/python/ref_dictionary_items.asp
    spots_per_time_list = [
        {'date': date, 
        'time': time, 
        'reserved_spots': data['reserved_spots'], 
        'available_spots': data['available_spots']
        } 
        for (date, time), data in spots_per_time.items()
    ]

    if request.method == 'POST':
        if 'delete' in request.POST:
            reservation_id = request.POST.get('reservation_id')
            reservation = get_object_or_404(Reservation, id=reservation_id)
            reservation.delete()
            messages.success(request, 'Reservation has been canceled')
            return redirect('reservations:list_reservation')

    return render(request, 'reservations/list_reservation.html', {
        'spots_per_time_list': spots_per_time_list,
        'reservations': reservations, 
    })


@login_required
@user_passes_test(is_admin_user)
def edit_reservation(request, reservation_id): # Ev ta bort
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request,'Reservation has been updated.')
            return redirect('reservations:list_reservation')
    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'reservations/edit_reservation.html', {
        'form': form,
        'reservation': reservation.email
    })
    
@login_required
def create_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            number_of_guests = form.cleaned_data['number_of_guests']

            # Check to see how many seats are available
            existing_reservations = Reservation.objects.filter(date=date, 
            time=time).aggregate(Sum('number_of_guests'))
            booked_seats =  existing_reservations['number_of_guests__sum'] or 0

            if booked_seats + number_of_guests <= 50:
                new_reservation = form.save(commit=False)
                new_reservation.email = request.user.email # Test
                new_reservation.reservation_name = request.user.username # Test
                new_reservation.save()

                return redirect('reservations:success_reservation', pk=new_reservation.pk)
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

#def list_reservations(request):
 #   reservations = Reservation.objects.all()
  #  return render(request, 'reservations/list_reservation.html', {'reservations': reservations})

def booking_management(request):
    return render(request, 'reservations/booking_management.html')

@login_required
def change_reservation(request):
    #Logic to handle change of reservation
    return render(request, 'reservations/contact_us.html')




