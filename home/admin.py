# Importing the admin module from Django
from django.contrib import admin
# Importing the MenuItem and MenuCategory models
from .models import MenuItem, MenuCategory


# Make MenuItem available in the admin panel
admin.site.register(MenuItem)
# Make MenuCategory available in the admin panel
admin.site.register(MenuCategory)
