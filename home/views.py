from django.shortcuts import render, redirect
from django.contrib.auth.models import User # To handle userdata
from django.contrib.auth import login # To log the user in after registration
from django.contrib import messages # Display messages
from django.conf import settings #To use settings

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
        # check if user exist
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken")
            return render(request, 'register.html')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            messages.success(request, "Registraion was successful")
            return redirect('home')
    return render(request, 'home/register.html')

def login(request):
    return render(request, 'home/login.html')
    