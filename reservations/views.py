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
from datetime import timedelta
# Django for handling timezones 
from django.utils import timezone

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
    # Retrieves the current time
    now = timezone.localtime()
    # Delete old reservations
    Reservation.objects.filter(date__lt=now.date()).delete()  
    Reservation.objects.filter(date=now.date(), time__lt=now.time()).delete()
    
    # Handle POST requests
    if request.method == 'POST' and 'delete' in request.POST:
        reservation_id = request.POST.get('reservation_id')
        reservation = get_object_or_404(Reservation, id=reservation_id)

        # Skicka avbokningsmejl
        try:
            send_mail(
                'Your reservation has been canceled',
                f"Hello {reservation.reservation_name},\n\nYour reservation for {reservation.date} at {reservation.time} has been canceled.",
                settings.DEFAULT_FROM_EMAIL,
                [reservation.email],
                fail_silently=False,
            )
            messages.success(request, "Cancellation email sent.")
        except Exception as e:
            messages.error(request, f"Failed to send cancellation email: {e}")

        # Ta bort reservationen
        reservation.delete()
        messages.success(request, 'Reservation has been canceled.')
        return redirect('reservations:list_reservation')

    # Retrieve remaining reservations
    reservations = Reservation.objects.all()

    # Group reservation logic by date and time
    spots_per_time = defaultdict(lambda: {'reserved_spots': 0, 'available_spots': 50})

    # Loop through group reservations by date and time, storing emails.
    for res in reservations:
        key = (res.date, res.time)
        spots_per_time[key]['reserved_spots'] += res.number_of_guests
        spots_per_time[key]['available_spots'] = 50 - spots_per_time[key]['reserved_spots']
        spots_per_time[key]['email'] = res.email

    # Convert to a list to send to the template
    spots_per_time_list = [
        {
            'date': date, 
            'time': time, 
            'reserved_spots': data['reserved_spots'], 
            'available_spots': data['available_spots'],
            'email': data['email']
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
            total_seats = 50
            available_seats = total_seats - booked_seats

            # Ensure total number of booked seats doesn´t exceed 50
            if available_seats <= 0:
                messages.error(request, "The selected time is fully booked")
            elif number_of_guests > available_seats:
                messages.error(request, f"Only {available_seats} seats are available for the chosen time")
            else:
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
                # Show error message 
                messages.error(request, "Something went wrong with the form.")
       
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
        reservation_id = request.GET.get('reservation_id')  
        if reservation_id:
            reservation = get_object_or_404(Reservation, id=reservation_id)  
        
    if request.method == 'POST':
        reservation_id = request.POST.get('reservation_id')  
        message = request.POST.get('message')  
        # Send email
        send_mail(
            subject=f"Change request for reservation {reservation_id}",
            message=f"Message from: {request.user.email}\n\n{message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        
        messages.success(request, 'Your request has been sent')
        #return redirect('reservations:success_reservation', pk=reservation_id) if reservation_id else redirect('reservations:logged_in_user')
        return redirect('reservations:success_email')
    
    return render(request, 'reservations/contact_us.html', {'reservation': reservation})


@login_required
def success_email(request):
   return render(request, 'reservations/success_email.html')


@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_reservation(request, reservation_id):
    # Retrive current reservation
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    if request.method == 'POST':
        # Retrieve updated data from the form
        reservation_name = request.POST.get('reservation_name')
        date = request.POST.get('date')
        time = request.POST.get('time')
        number_of_guests = request.POST.get('number_of_guests')

        # Update reservation with new data
        reservation.reservation_name = reservation_name
        reservation.date = date
        reservation.time = time
        reservation.number_of_guests = number_of_guests
        reservation.save()

        # Send confirmation email after the update   
        try:
            send_mail(
                'Your reservation has been updated',
                'Your reservation has been updated. Check under \'My reservation\' to see your current reservation.',
                settings.DEFAULT_FROM_EMAIL,
                [reservation.email],
                fail_silently=False,
            )
                 
            messages.success(request, "Test email sent.")
        except Exception as e:
            messages.error(request, "Failed to send confirmation email.")

        messages.success(request, 'Reservation has been updated.')

        return redirect('reservations:list_reservation')
    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'reservations/edit_reservations.html', {'form': form, 'reservation': reservation})



def users_reservations(request):
    user_reservations = Reservation.objects.filter(email=request.user.email)
    return render(request, 'reservations/users_reservations.html', {'reservations': user_reservations})

def sitting_time():
    return timedelta(hours=1.5)
