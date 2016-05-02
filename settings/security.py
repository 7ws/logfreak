from decouple import Csv, config


# Key for salting hashes and such
SECRET_KEY = config('SECRET_KEY', default='changeme')

# Host names allowed when DEBUG=False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=Csv())

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator'),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'),
    },
]


# Oauth parameters for the Twitter API
# Required access level: "Read, write, and direct messages"
# See https://dev.twitter.com/oauth/overview/application-owner-access-tokens
TWITTER_CONSUMER_KEY = config('TWITTER_CONSUMER_KEY', default='')
TWITTER_CONSUMER_SECRET = config('TWITTER_CONSUMER_SECRET', default='')
