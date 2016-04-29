from decouple import config

from .base import BASE_DIR


# URL to serve static files
STATIC_URL = config('STATIC_URL', default='/static/')

STATICFILES_DIRS = [
    BASE_DIR.child('frontend'),
]
