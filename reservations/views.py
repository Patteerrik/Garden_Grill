from django.shortcuts import render, get_object_or_404, redirect 
# Render Template, get object or 404, redirect users
from django.contrib.auth.decorators import login_required, user_passes_test
# Resrict access to logged in or admin users
from .models import Reservation
# Import reservation model
from .forms import ReservationForm
# Import reservationform for bookings
from django.contrib import messages 
# To show messages to the user
from django.conf import settings
# Access django settings
from django.db.models import Sum 
# To summarize number of guests
from django.core.mail import send_mail
# Send emails with django
from collections import defaultdict
# Dictionary with deafult values

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
@user_passes_test(is_admin_user)
def list_reservation(request):
    reservations = Reservation.objects.all()
    # Handle POST requests
    if request.method == 'POST':
        reservation_id = request.POST.get('reservation_id')
        reservation = get_object_or_404(Reservation, id=reservation_id)
        
        # Handle reservation edits
        if 'edit' in request.POST:
            number_of_guests = request.POST.get('number_of_guests')
            reservation.number_of_guests = number_of_guests
            reservation.save()
            messages.success(request, 'Reservation has ben updated.')
            return redirect('reservations:list_reservation')
        # Handle delition of reservations
        elif 'delete' in request.POST:
            reservation.delete()
            messages.success(request, 'Reservations has been canceled.')
            return redirect('reservations:list_reservation')
    

    # Group reservation logic by date and time
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

    return render(request, 'reservations/list_reservation.html', {
        # Send a summary of seats to template
        'spots_per_time_list': spots_per_time_list,
        # Sends booking to template 
        'reservations': reservations, 
    })
    
@login_required
def create_reservation(request):
    # Check if the request method is POST
    if request.method == 'POST':
        # Bind the form with post data
        form = ReservationForm(request.POST)
        if form.is_valid():
            # Extract cleaned data from the form
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            number_of_guests = form.cleaned_data['number_of_guests']

            # Check to see how many seats are available
            existing_reservations = Reservation.objects.filter(date=date, 
            time=time).aggregate(Sum('number_of_guests'))
            booked_seats =  existing_reservations['number_of_guests__sum'] or 0

            # Ensure total number of booked seats doesn´t exceed 50
            if booked_seats + number_of_guests <= 50:
                # Save the form without committing
                new_reservation = form.save(commit=False)
                # Set email and username for new reservation
                new_reservation.email = request.user.email 
                # Set email and username for reservation
                new_reservation.reservation_name = request.user.username
                # Save the reservation to the database
                new_reservation.save()

                # Redirect to success page after reservation is created
                return redirect('reservations:success_reservation', pk=new_reservation.pk)
            else:
                # Show error message if there is not not enough avaible seats
                messages.error(request, f"Only {50 - booked_seats} seats are available for the selected time.")
        else:
            # Show error message if the form is invalid
            messages.error(request, f" There was an error in the form. Please try again")
    else:
        # If the request is not POST, display an empty form
        form = ReservationForm()
    # Display the reservation form
    return render(request, 'reservations/create_reservation.html', {'form': form})


def success_reservation(request, pk):
    # Retrieve the reservation by pk or return 404 if not found
    reservation = get_object_or_404(Reservation, pk=pk)
    # Display the success page with reservation details
    return render(request, 'reservations/success_reservation.html', {'reservation': reservation})

@login_required
def change_reservation(request):
    reservation = None  # Default reservation to None
    if request.method == 'GET':
        reservation_id = request.GET.get('reservation_id')  # Hämta reservation_id från GET
        if reservation_id:
            reservation = get_object_or_404(Reservation, id=reservation_id)  
        

    if request.method == 'POST':
        reservation_id = request.POST.get('reservation_id')  
        message = request.POST.get('message')  
        # Skicka mejlet
        send_mail(
            subject=f"Change request for reservation {reservation_id}" if reservation_id else "General change request",
            message=message,
            from_email=request.user.email,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        
        messages.success(request, 'Your request has been sent')
        return redirect('reservations:success_reservation', pk=reservation_id) if reservation_id else redirect('reservations:logged_in_user')

    
    return render(request, 'reservations/contact_us.html', {'reservation': reservation})






