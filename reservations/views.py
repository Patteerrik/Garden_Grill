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
from datetime import timedelta, datetime
# Django for handling time and date
from django.utils import timezone
# To work with timezones and local times
from django.contrib.auth import get_user_model
# Get the user model dynamically, instead of importing it directly
from django.contrib.messages import get_messages
# Used to get and display messages to users
from django import forms
# Import Django's form
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def logged_in_user(request):
    # check if user is admin
    if request.user.is_staff:
        # If the user is an admin, show the admin page
        return render(request, 'reservations/logged_in_admin.html')
    else:
        # If user is not admin show user page
        return render(request, 'reservations/logged_in_user.html')

@csrf_exempt
def is_admin_user(user):
    # Return True if the user is an admin, False if not
    return user.is_staff


# @login_required
@csrf_exempt
def logged_in_admin(request):
    # Show the admin page for logged-in admins
    return render(request, 'reservations/logged_in_admin.html')


#@login_required
#@user_passes_test(is_admin_user)
@csrf_exempt
def list_reservation(request):
    # Retrieves the current time
    now = timezone.localtime()

    # Delete old reservations
    Reservation.objects.filter(date__lt=now.date()).delete()
    Reservation.objects.filter(date=now.date(), time__lt=now.time()).delete()

    # Handle POST requests for reservation deletion
    if request.method == 'POST' and 'delete' in request.POST:
        reservation_id = request.POST.get('reservation_id')
        reservation = get_object_or_404(Reservation, id=reservation_id)

        # Try sending a cancellation email and delete the reservation
        try:
            send_mail(
                'Your reservation has been canceled',
                f"Hello {reservation.reservation_name},\n\n"
                f"Your reservation for {reservation.date} at "
                f"{reservation.time} has been canceled.",
                settings.DEFAULT_FROM_EMAIL,
                [reservation.email],
                fail_silently=False,
            )
            # If email is sent, delete the reservation and show message
            reservation.delete()
            messages.success(
                request,
                "Reservation has been canceled. "
                "Cancellation email sent.")
        except Exception as e:
            # If email fails to send, show an error message
            messages.error(request, f"Failed to send cancellation email: {e}")

        # Redirect to the reservation list page
        return redirect('reservations:list_reservation')

    # Retrieve remaining reservations
    reservations = Reservation.objects.all()

    # Group reservations by date and time, and shows available spots
    spots_per_time = defaultdict(
        lambda: {'reserved_spots': 0, 'available_spots': 50}
    )

    # Loop through the reservations, updating reserved and available spots
    for res in reservations:
        key = (res.date, res.time)
        spots_per_time[key]['reserved_spots'] += res.number_of_guests
        spots_per_time[key]['available_spots'] = (
            50 - spots_per_time[key]['reserved_spots']
        )
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

    # Display the list of reservations and available seat summaries
    return render(request, 'reservations/list_reservation.html', {
        # Seat summary
        'spots_per_time_list': spots_per_time_list,
        # Reservation details
        'reservations': reservations,
    })


#@login_required
@csrf_exempt
def create_reservation(request):
    # Check if the request method is POST
    if request.method == 'POST':
        form = ReservationForm(request.POST)

        # Process the form if it's valid
        if form.is_valid():
            new_reservation = process_reservation_form(request, form)

            # If the reservation is successfull, send confirmation email
            if new_reservation:
                send_reservation_conf_email(new_reservation)
                return redirect(
                    'reservations:success_reservation',
                    pk=new_reservation.pk  # Redirect to the success page
                )

        else:
            # If the form is invalid, show error messages for each field
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

            # Re-render the reservation creation page with the form
            return render(
                request,
                'reservations/create_reservation.html',
                {'form': form}
            )

    else:
        # Set up initial form data with default or empty values
        initial_data = {
            'reservation_name': '',
            'email': '' if request.user.is_staff else request.user.email,
            'time': '',
            'number_of_guests': ''
        }

        form = ReservationForm(initial=initial_data)

        # If the user is staff, make the email field required
        if request.user.is_staff:
            form.fields['email'].required = True
    # Render the reservation creation page with the form
    return render(
        request,
        'reservations/create_reservation.html',
        {'form': form}
    )

@csrf_exempt
def send_reservation_conf_email(reservation):
    """
    Sends a confirmation email to the user after the reservation is saved.
    This function is separated to keep the create_reservation view cleaner.
    """
    subject = 'Reservation Confirmation'
    message = (
        f"Your reservation for {reservation.date} at {reservation.time} "
        "has been successfully made."
    )
    recipient_list = [reservation.email]

    # Send the email with the reservation details
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        # If set to False, raises an error if email fails to send
        fail_silently=False,
    )

@csrf_exempt
def process_reservation_form(request, form):
    """
    Handles the form and creates a new reservation.
    Manages validation and email assignment.
    Returns the reservation if successful, otherwise None.
    This function is separated to keep the create_reservation view cleaner.
    """
    if form.is_valid():
        date = form.cleaned_data['date']
        time = form.cleaned_data['time']
        number_of_guests = form.cleaned_data['number_of_guests']

        # Check if there are enough available seats
        is_available, message = check_availability(
            date, time, number_of_guests
        )

        if not is_available:
            messages.error(request, message)
            return None

        # Create a new reservation if there are enough available seats
        new_reservation = form.save(commit=False)
        new_reservation.reservation_name = (
            form.cleaned_data.get('reservation_name', request.user.username)
        )

        # Assign email based on user type
        if request.user.is_staff:
            new_reservation.email = form.cleaned_data['email']
        else:
            new_reservation.email = request.user.email

        new_reservation.save()
        return new_reservation

    return None

@csrf_exempt
def check_availability(date, time, number_of_guests):
    """
    Checks availability for a specific date and time within a 1.5 hour window.
    Returns (is_available, message) with availability status.
    """
    total_seats = 50  # Maximum number of seats per sitting
    sitting_duration = timedelta(minutes=90)  # 1,5 hours

    # Define the time range for 1.5 hours before and after the booking
    start_time = datetime.combine(date, time) - sitting_duration
    end_time = datetime.combine(date, time) + sitting_duration

    # Get bookings within the 1.5-hour time window
    existing_reservations = Reservation.objects.filter(
        date=date,
        time__gte=start_time.time(),
        time__lte=end_time.time()
    ).aggregate(Sum('number_of_guests'))

    booked_seats = existing_reservations['number_of_guests__sum'] or 0
    available_seats = total_seats - booked_seats

    # If a user tries to book more than 50 seats in one booking
    if number_of_guests > total_seats:
        return False, "The selected time is fully booked."

    # Check if all seats are booked
    if available_seats <= 0:
        return False, "The selected time is fully booked."

    # Check if the user's booking exceeds available seats
    elif number_of_guests > available_seats:
        return False, (
            f"Only {available_seats} seats are available for the chosen time."
        )

    return True, None

@csrf_exempt
def success_reservation(request, pk):
    # Retrieve the reservation by pk or return 404 if not found
    reservation = get_object_or_404(Reservation, pk=pk)
    # Display the success page with reservation details
    return render(
        request, 'reservations/success_reservation.html',
        {'reservation': reservation}
    )


#@login_required
@csrf_exempt
def change_reservation(request):
    # Check if the request method is POST
    if request.method == 'POST':
        # Get username, email, and message from the submitted form
        username = request.POST.get('username')
        email = request.POST.get('email')
        message_content = request.POST.get('message')

        # Store the form data in a context dictionary
        context = {
            'username': username,
            'email': email,
            'message_content': message_content,
        }

        # Check if both username and email are provided
        if not username or not email:
            # If either is missing, show an error message
            messages.error(request, 'Both username and email are required.')
            return render(request, 'reservations/contact_us.html', context)

        User = get_user_model()
        try:
            # Try to find the user by username and email
            user = User.objects.get(username=username, email=email)
        except User.DoesNotExist:
            # If no matching user, show an error message
            messages.error(request, 'Invalid username or email.')
            return render(request, 'reservations/contact_us.html', context)

        # Check if message content is at least 10 characters
        if not message_content or len(message_content) < 10:
            # Show an error message if the message is too short
            messages.error(
                request,
                'Message must be at least 10 characters long.'
            )
            return render(request, 'reservations/contact_us.html', context)

        try:
            # Try to send an email with the message details
            send_mail(
                subject="Change request for reservation",
                message=f"Message from: {user.email}\n\n{message_content}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            # Show success message if email is sent
            messages.success
            (request, "Your request has been sent successfully.")
            return redirect('reservations:success_email')

        except Exception as e:
            # Show an error if the email could not be sent
            messages.error(request, f"Failed to send message: {str(e)}")
            return render(request, 'reservations/contact_us.html', context)

    return render(request, 'reservations/contact_us.html')


#@login_required
@csrf_exempt
def success_email(request):
    # Render the success page after reservation email is sent
    return render(request, 'reservations/success_email.html')


#@login_required
#@user_passes_test(lambda u: u.is_staff)
@csrf_exempt
def edit_reservation(request, reservation_id):
    # Retrieve the reservation by ID or show 404 if not found
    reservation = get_object_or_404(Reservation, id=reservation_id)

    # Handle form submission when the method is POST
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

        # Try sending confirmation email after the update
        try:
            send_mail(
                'Your reservation has been updated',
                'Your reservation has been updated. '
                'Check under \'My reservation\' '
                'to see your current reservation.',
                settings.DEFAULT_FROM_EMAIL,
                [reservation.email],
                fail_silently=False,
            )

            # Show a success message and redirect to the reservation list
            messages.success(
                request,
                'Reservation has been updated. '
                'A confirmation email has been sent.'
            )
            return redirect('reservations:list_reservation')
        # If the email fails to send, display an error message
        except Exception as e:
            messages.error(
                request,
                'Failed to send confirmation email. Reservation was updated, '
                'but email was not sent.'
            )
    # Display the reservation form with existing reservation details
    form = ReservationForm(instance=reservation)
    return render(
        request,
        'reservations/edit_reservations.html',
        {'form': form, 'reservation': reservation}
    )

@csrf_exempt
def users_reservations(request):
    # Get all reservations for the logged-in user
    user_reservations = Reservation.objects.filter(email=request.user.email)

    # Render the user's reservations page with the list of their reservations
    return render(
        request,
        'reservations/users_reservations.html',
        {'reservations': user_reservations}
    )


def sitting_time():
    # Return the duration of a sitting, which is 1.5 hours
    return timedelta(hours=1.5)
