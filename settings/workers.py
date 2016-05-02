from decouple import config


RQ_QUEUES = {
    'default': {
        'URL': config('REDIS_URL', 'redis://localhost:6379/0'),
    },
}
