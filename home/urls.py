from django.urls import path, include
# Import views module from current directory
from . import views
# Import handlers for 404 and 500 errors
from django.conf.urls import handler404, handler500
# Import specific view for logging out
from .views import logout_view


# Define the mapping between URLs and view functions
urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu_view, name='menu'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
]
