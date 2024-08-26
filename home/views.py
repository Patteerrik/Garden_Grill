from django.shortcuts import render
from django.conf import settings

# Create your views here.
def home(request):
    context = {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'home/index.html', context)

def hello(request):
    return render(request, 'home/hello.html')
