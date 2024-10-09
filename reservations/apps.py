from django.apps import AppConfig
# Import the AppConfig class to configure the app

class ReservationsConfig(AppConfig):
    # This class configures the reservations app
    default_auto_field = 'django.db.models.BigAutoField'
    # Specifies the default auto field type for models in the app
    name = 'reservations'
    # The name of the app
