from django.shortcuts import render, redirect
from django.contrib.auth.models import User # To handle userdata
from django.contrib.auth import authenticate, login # To log the user in after registration
from django.contrib import messages # Display messages
from django.conf import settings #To use settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model 
from django.core.mail import send_mail

# Create your views here.
def home(request):
    context = {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'home/index.html', context)

def hello(request):
    return render(request, 'home/hello.html')

def bookings(request):
    return render(request, 'home/bookings.html')

def menu(request):
    return render(request, 'home/menu.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        
        if get_user_model().objects.filter(username=username).exists():
            return render(request, 'home/register.html', {'error': 'Username already exists'})

        if get_user_model().objects.filter(email=email).exists():
            return render(request, 'home/register.html', {'error': 'Email already exists'})

        user = get_user_model().objects.create_user(username=username, email=email, password=password)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            print("Försöker skicka bekräftelsemail...") # Debug
            try:
                send_mail(
                    'Confirmation of registration',
                    f'Thank you {username} for signing up!',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False
                )
                print("E-post skickades!") # Debug
            except Exception as e:
                print(f"E-post misslyckades: {str(e)}") # Debug

            return redirect('reservations:logged_in_user')
        else:
            return render(request, 'home/register.html', {'error': 'Authentication failed'})

    return render(request, 'home/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')

            if user.username == 'admin0110':
                return redirect('reservations:logged_in_admin')
            elif user.is_staff:
                return redirect('reservations:logged_in_admin')
            else:
                return redirect('reservations:logged_in_user')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'home/login.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:  # Checks if user is admin
            login(request, user)
            return redirect('booking_management')  # Redirect to booking management page
        else:
            messages.error(request, 'Invalid credentials or not authorized')
    return render(request, 'home/admin_login.html')



    