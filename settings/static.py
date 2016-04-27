from decouple import config


# URL to serve static files
STATIC_URL = config('STATIC_URL', default='/static/')
