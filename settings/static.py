from decouple import config

from .base import BASE_DIR, DEBUG


# URL to serve static files
STATIC_URL = config('STATIC_URL', default='/static/')

# Directories to find static files
STATICFILES_DIRS = [
    BASE_DIR.child('frontend', 'static'),
]

# Directories to save media and compiled static files
MEDIA_ROOT = BASE_DIR.child('.public', 'media')
STATIC_ROOT = BASE_DIR.child('.public', 'static')

# Static files storage engine
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'


# Static files finding engines
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
]


# Static files groups
PIPELINE = {
    # Style files
    'STYLESHEETS': {
        '3rd-party': {
            'source_filenames': [
            ],
            'output_filename': '_compiled/css/3rd-party.css'
        }
    },

    # JavaScript files
    'JAVASCRIPT': {
        '3rd-party': {
            'source_filenames': [
            ],
            'output_filename': '_compiled/js/3rd-party.js'
        }
    },

    # Compressors
    'CSS_COMPRESSOR': 'pipeline.compressors.cssmin.CSSMinCompressor',
    'JS_COMPRESSOR': 'pipeline.compressors.jsmin.JSMinCompressor',
}


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
