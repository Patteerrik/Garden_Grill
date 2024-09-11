from django.shortcuts import render, redirect
from django.contrib.auth.models import User # To handle userdata
from django.contrib.auth import authenticate, login, logout # To log the user in after registration
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
    print(request.POST)  
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']

        if password != confirm_password:
            print("Passwords do not match")
            return render(request, 'home/register.html', {'error': 'Passwords do not match'})

        
        if get_user_model().objects.filter(username=username).exists():
            print("Username already exists")  
            return render(request, 'home/register.html', {'error': 'Username already exists'})

        if get_user_model().objects.filter(email=email).exists():
            print("Email already exists")
            return render(request, 'home/register.html', {'error': 'Email already exists'})

        user = get_user_model().objects.create_user(username=username, email=email, password=password)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            try:  
                send_mail(
                    'Confirmation of Registration',
                    f'Thank you {username} for registering at Garden and Grill!',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False
                )
                print('Email was sent!')
            except Exception as e:
                print(f"Error sending email: {str(e)}")
           
            if user.username == 'admin0011' or user.is_staff:
                print('Redirect to admin.')
                return redirect('reservations:logged_in_admin')
            else:
                print('Redirect to user')
                return redirect('reservations:logged_in_user')

    return render(request, 'home/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')

            # Kontrollera om det är admin eller vanlig användare
            if user.username == 'admin0011' or user.is_staff:
                return redirect('reservations:logged_in_admin')
            else:
                return redirect('reservations:logged_in_user')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'home/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login') # Redirect to login page after logout




    