from decouple import config

from .base import BASE_DIR, DEBUG


# URL to serve static files
STATIC_URL = config('STATIC_URL', default='/static/')

# Directories to find static files
STATICFILES_DIRS = [
    BASE_DIR.child('frontend'),
]

# Template finders and processors
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR.child('frontend', 'templates'),
        ],
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request'
            ],
            'loaders': [
                ('pyjade.ext.django.Loader', [
                    'django.template.loaders.filesystem.Loader',

                    # Support 3rd-party apps
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
            'builtins': ['pyjade.ext.django.templatetags'],
        },
    },
]
