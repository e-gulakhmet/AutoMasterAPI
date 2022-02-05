from .local import *

DEBUG = True

SECRET_KEY = 'test)(r$zokmzkv)6=jrwe6vu)94as0(^&-l%4mya4inm%#b1^_gf+'

PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']

# SECURE_AUTH_SALT should not contain $
SECURE_AUTH_SALT = '1_n=qJO51@GW%kqewWphc-`]*3@6336H7sxhogE5tSO|aoM|3Q(zD3.+%E}~p<L'
