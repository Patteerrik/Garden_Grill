from django.shortcuts import render, redirect
from django.contrib.auth.models import User # To handle userdata
from django.contrib.auth import authenticate, login, logout # To log the user in after registration
from django.contrib import messages # Display messages
from django.conf import settings #To use settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model 
from django.core.mail import send_mail
from .models import MenuCategory
from django.http import HttpResponse # Test

# Create your views here.
def home(request):
    return render(request, 'base.html', {})

def bookings(request): # Remove?
    return render(request, 'home/bookings.html')

def menu(request):
    return render(request, 'home/menu.html')


def register(request):  
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']

        # Check if passwords matches
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        # Check is username already exists
        if get_user_model().objects.filter(username=username).exists(): 
            messages.error(request, 'Username already exists.') 
            return redirect('register')

        
        # Check if email already exists
        if get_user_model().objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')
        
        # Create user
        user = get_user_model().objects.create_user(username=username, email=email, password=password)
        
        # Authencticate and log the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            # Send email verification
            try:  
                send_mail(
                    'Confirmation of Registration',
                    f'Thank you {username} for registering at Garden and Grill!',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False
                )
            except Exception as e:
                messages.error(request, f"Failed to send confirmation email: {e}")

            # Redirect after logged in status
            if user.username == 'admin0011' or user.is_staff:
                return redirect('reservations:logged_in_admin')
            else:
                return redirect('reservations:logged_in_user')

    return render(request, 'home/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # Check if admin or user
            if user.username == 'admin0011' or user.is_staff:
                return redirect('reservations:logged_in_admin')
            else:
                return redirect('reservations:logged_in_user')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'home/login.html')


def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('home') # Redirect to login page after logout


def menu_view(request):
    categories = MenuCategory.objects.prefetch_related('menu_items').all()
    return render(request, 'home/menu.html', {'categories': categories})

from django.http import HttpResponse







    