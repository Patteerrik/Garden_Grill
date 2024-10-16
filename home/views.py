from django.shortcuts import render, redirect
# To log the user in after registration
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages  # Display messages
from django.conf import settings  # To use settings
# Restrict access to logged-in users
from django.contrib.auth.decorators import login_required
# Get the custom or default User model
from django.contrib.auth import get_user_model
# Send email functionality
from django.core.mail import send_mail
# Import the MenuCategory model
from .models import MenuCategory
# Django's built-in User model
from django.contrib.auth.models import User
# Raise validation errors
from django.core.exceptions import ValidationError
# Validate email format
from django.core.validators import validate_email


# Home view, renders the base.html template
def home(request):
    return render(request, 'base.html', {})


# Handles user registration
def register(request):
    # If the form is submitted via POST
    if request.method == 'POST':
        email = request.POST.get('email', '')  # Get email
        username = request.POST.get('username', '')  # Get username
        password = request.POST.get('password', '')  # Get password
        # Confirm passsword
        confirm_password = request.POST.get('confirm_password', '')

        # Keep form data if validation fails
        context = {
            'email': email,
            'username': username,
        }

        # Validate th email format
        try:
            validate_email(email)

            #
            local_part, domain_part = email.rsplit('@', 1)
            domain_name, tld = domain_part.rsplit('.', 1)

            # Ensure minimum length requirements
            if len(local_part) < 2 or len(domain_name) < 2 or len(tld) < 2:
                raise ValidationError('Email is not valid.')

        except ValidationError:
            # If validation fails, show an error message
            messages.error(request, 'Email is not valid.')
            return render(request, 'home/register.html', context)

        # Check if email already exists in the database
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'home/register.html', context)

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'home/register.html', context)

        # Ensure both passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'home/register.html', context)

        # Create the user if all checks pass
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password if password else None
        )
        # Success message and redirect to login page
        messages.success(request, f"Welcome, {username}!")
        return redirect('login')

    # Show the registration form
    return render(request, 'home/register.html')


# Login view
def login_view(request):
    # If the form is submitted via POST
    if request.method == 'POST':
        username = request.POST.get('username', '')  # Get username
        password = request.POST.get('password', '')  # Get password

        # Authenticate the user based on the entered credentials
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # If credentials correct, log user in and redirect to the homepage
            login(request, user)
            return redirect('reservations:logged_in_user')
        else:
            # If credentials are incorrect, show an error message
            messages.error(request, 'Invalid username or password')
            return render(request, 'home/login.html', {
                'username': username,
            })

    # Show the login form
    return render(request, 'home/login.html')


# Logout view
def logout_view(request):
    logout(request)  # Log out user
    request.session.flush()  # Clear session data
    return redirect('home')  # Redirect to login page after logout


# Menu view
def menu_view(request):
    # Gets menu categories with related items
    categories = MenuCategory.objects.prefetch_related('menu_items').all()
    # Show menu page with categories
    return render(request, 'home/menu.html', {'categories': categories})
