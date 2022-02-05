from .common import *

DEBUG = True

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'stage)(r$zokmzkv)6=jrde6vu)94as0(^&-l%4mya4inm%#b1^_gf+')
SECURE_AUTH_SALT = os.environ.get('SECURE_AUTH_SALT',
                                  'stage1_n=qJO51@GW%kqewWphc-`]*3$@6336H7sxhogE5tSO|aoM|3Q(zD3.+%E}~p<L')

BASE_URL = os.environ.get('BASE_URL', '')
BASE_CLIENT_URL = os.environ.get('BASE_CLIENT_URL', '')

# SECURITY WARNING: update this when you have the production host
ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS',
    'localhost,server-main').split(',')

LOG_PATH = os.path.join(BASE_DIR, '../logs')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/debug.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'celery': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/celery.log',
            'formatter': 'verbose',
            'maxBytes': 1024 * 1024 * 100,  # 100 mb
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'celery': {
            'handlers': ['celery', 'console'],
            'level': os.getenv('CELERY_LOG_LEVEL', 'INFO'),
        },
    },
}


STATIC_URL = '/static/'
MEDIA_PATH = 'media'
MEDIA_URL = '%s/%s/' % (BASE_URL, MEDIA_PATH)
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')