from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Reservation
from .forms import ReservationForm
from django.contrib import messages # To show messages to the user
from django.conf import settings
from django.db.models import Sum # To summarize number of guests
from django.core.mail import send_mail


def is_admin_user(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin_user)
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
    total_spots = 50
    reserved_spots = sum([res.number_of_guests for res in reservations])
    available_spots = total_spots - reserved_spots

    if request.method == 'POST':
        if 'delete' in request.POST:
            reservation_id = request.POST.get('reservation_id')
            reservation = get_object_or_404(Reservation, id=reservations_id)
            reservation.delete()
            messages.success(request, 'Reservation has been canceled')
            return redirect('list_reservation')

    return render(request, 'reservations/list_reservation.html', {
    'reservations': reservations,
    'available_spots': available_spots,
    'total_spots': total_spots,
    'reserved_spots': reserved_spots,
})


@login_required
@user_passes_test(is_admin_user)
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request,'Reservation has been updated.')
            return redirect('list_reservation')
    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'reservations/edit_reservation.html', {'form': form})
    
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

# Defining registration
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        
        if get_user_model().objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})

        if get_user_model().objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already exists'})

        user = get_user_model().objects.create_user(username=username, email=email, password=password)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            send_mail(
                'Confirmation of registration',
                f'Thank you {username} for signing up!',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False
            )

            return redirect('logged_in_user')
        else:
            return render(request, 'register.html', {'error': 'Authentication failed'})

    return render(request, 'register.html')

def logged_in_user(request):
    # check if user is admin
    if request.user.is_staff:
        return render(request, 'reservations/logged_in_admin.html')
    else:
        # If user is not admin show user page
        return render(request, 'reservations/logged_in_user.html')

def success_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(request, 'reservations/success_reservation.html', {'reservation': reservation})

def list_reservations(request):
    reservations = Reservation.objects.all()
    return render(request, 'reservations/list_reservation.html', {'reservations': reservations})

def booking_management(request):
    return render(request, 'reservations/booking_management.html')




