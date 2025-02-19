"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 4.2.15.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""


# Imports OS module
import os
# Imports Path class for handling file and directory paths
from pathlib import Path
# External library for handling the database URL
import dj_database_url
# For reading environment variables securely
from decouple import config

import sys  # TEST


# Load environment variables if the env.py file exists
if os.path.isfile('env.py'):
    import env


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


# List of allowed hosts for the project to handle
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "gardengrill-d40b8e344381.herokuapp.com"
]


# Email backend configuration using Gmail's SMTP server
# https://medium.com/django-unleashed/email-configuration-in-django-3c7d9e149445
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # Custom applications
    'home',
    'reservations',

    # Form handling with Crispy Forms and Bootstrap 5
    'crispy_forms',
    'crispy_bootstrap5',

]

# Site framework
SITE_ID = 1

# Restaurant's maximum seating capacity
MAX_SEATS = 50

# Admin email for reservation notifications
ADMIN_EMAIL = os.getenv('EMAIL_HOST_USER')


MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

CACHE_MIDDLEWARE_SECONDS = 0
CACHE_MIDDLEWARE_KEY_PREFIX = 'gardengrill'

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

# Crispy forms settings
CRISPY_TEMPLATE_PACK = 'bootstrap5'
CRISPY_ALLOWED_TEMPLATE_PACKS = ('bootstrap5')


# Root URL configuration
ROOT_URLCONF = 'main.urls'


# Template settings for rendering HTML pages
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Authentication backends for both Django admin and allauth
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

# WSGI application entry point
WSGI_APPLICATION = 'main.wsgi.application'


# Database configuration, using dj_database_url
DATABASES = {
    'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
}
# Use SQLite for testing
if 'test' in sys.argv:
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'

# Trusted origins for CSRF protection
CSRF_TRUSTED_ORIGINS = [
    "https://localhost",
    "https://gardengrill-d40b8e344381.herokuapp.com"
]


# Password validation settings
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
            'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization and localization settings
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
# Timezone set to Stockholm
TIME_ZONE = 'Europe/Stockholm'
# Enable internationalizatio
USE_I18N = True
# Use timezone-aware dates and times
USE_TZ = True


# Session settings to expire sessions after inactivity
# End session after 10 minutes of inactivity
SESSION_COOKIE_AGE = 600
# End session when browser closes
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# Save the session after every request
SESSION_SAVE_EVERY_REQUEST = False


# https://www.youtube.com/watch?v=-E2igrFADI0
# Account
# Allow login by username or email
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_VERIFCATION = 'none'
ACCOUNT_USERNAME_MIN_LENGTH = 4  # Minimum length for username
LOGIN_REDIRECT_URL = 'home'  # Redirect successful login
LOGOUT_REDIRECT_URL = '/'  # Redirect after logout


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = '/static/'  # URL for static files
STATICFILES_DIRS = [
    BASE_DIR / 'main/static',  # Directory for static files
]
# Directory for collected static files
STATIC_ROOT = BASE_DIR / 'staticfiles'


# Use WhiteNoise for static file serving
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


COMPRESS_ROOT = BASE_DIR / 'staticfiles'

# Specify MIME types for CSS and JavaScript
WHITENOISE_MIMETYPES = {
    '.css': 'text/css',
    '.js': 'application/javascript',
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
