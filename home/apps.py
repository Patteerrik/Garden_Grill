# Import the AppConfig class to configure app settings
from django.apps import AppConfig


# Configuration class for the home app
class HomeConfig(AppConfig):
    # Specifies the default type for primary key fields
    default_auto_field = 'django.db.models.BigAutoField'
    # Name of the application
    name = 'home'
