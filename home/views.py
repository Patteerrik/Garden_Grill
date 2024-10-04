from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout # To log the user in after registration
from django.contrib import messages # Display messages
from django.conf import settings #To use settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model 
from django.core.mail import send_mail
from .models import MenuCategory
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    return render(request, 'base.html', {})


#def menu(request):
    #return render(request, 'home/menu.html')


from django.contrib.auth import get_user_model, authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        context = {
            'username': username,
            'email': email,
        }

        # Validering
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'home/register.html', context)

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'home/register.html', context)

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'home/register.html', context)

        
        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, f"Welcome, {username}!")
        return redirect('login')

    return render(request, 'home/register.html')




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'home/login.html', {
                'username': username,  
            })

    return render(request, 'home/login.html')


def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('home') # Redirect to login page after logout


def menu_view(request):
    categories = MenuCategory.objects.prefetch_related('menu_items').all()
    return render(request, 'home/menu.html', {'categories': categories})







    