"""
ASGI config for main project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

# Importing the os module
import os
# Importing 'get_asgi_application' to serve the ASGI app
from django.core.asgi import get_asgi_application
# Setting the default settings module for the 'main' project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
# Getting the ASGI application to be used by the server
application = get_asgi_application()
