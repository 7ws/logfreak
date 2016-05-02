from decouple import config
from dj_database_url import parse as db_url
from django.core.urlresolvers import reverse_lazy as r
from unipath import Path


# Basic (self-explanatory) definitions
BASE_DIR = Path(__file__).ancestor(2)
DEBUG = config('DEBUG', default=True, cast=bool)


# Active apps
INSTALLED_APPS = [
    'backend.webview',  # Put at first to override some Django built-ins

    # Django built-in apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'django_rq',
    'pipeline',
    'polymorphic',

    # Local apps
    'backend.base',
    'backend.sms_logger',
    'backend.twitter_logger',
]


# Active middlewares
MIDDLEWARE_CLASSES = [
    # Django built-in middlewares
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Third-party middlewares

    # Local middlewares
]


# URL and gateway config
ROOT_URLCONF = 'backend.urls'
WSGI_APPLICATION = 'backend.wsgi.application'


# Database
DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='sqlite:///{}'.format(BASE_DIR.child('db.sqlite3')),
        cast=db_url),
}


# Internationalization
LANGUAGE_CODE = config('LANGUAGE_CODE', default='en-us')
TIME_ZONE = config('TIME_ZONE', default='America/Sao_Paulo')
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Authentication URLs
LOGIN_URL = r('auth:login')
LOGIN_REDIRECT_URL = r('home')
