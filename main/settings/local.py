from .common import *

DEBUG = True

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'DJANGO_SECRET_KEY')

BASE_URL = os.environ.get('BASE_URL', 'http://localhost:4096')

# SECURITY WARNING: update this when you have the production host
ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1']
