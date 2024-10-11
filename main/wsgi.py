"""
WSGI config for main project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

# Import the os module
import os
# Import Django's get_wsgi_application
from django.core.wsgi import get_wsgi_application
# Set the default settings module for the 'main' project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
# Retrieve the WSGI application callable for use with WSGI servers
application = get_wsgi_application()
