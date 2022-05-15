from .base import *
import os

from decouple import config

DEBUG = False
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else ['*']
CSRF_TRUSTED_ORIGINS = ['https://'+ os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []

MIDDLEWARE = [                                                                   
    'django.middleware.security.SecurityMiddleware',
# Add whitenoise middleware after the security middleware                             
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',                      
    'django.middleware.common.CommonMiddleware',                                 
    'django.middleware.csrf.CsrfViewMiddleware',                                 
    'django.contrib.auth.middleware.AuthenticationMiddleware',                   
    'django.contrib.messages.middleware.MessageMiddleware',                      
    'django.middleware.clickjacking.XFrameOptionsMiddleware',                    
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')










# PRODUCTION_APPS = ['whitenoise.runserver_nostatic']

# DEVELOPMENT_MIDDLEWARE = [
#     'whitenoise.middleware.WhiteNoiseMiddleware',
# ]

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
STATIC_ROOT = (BASE_DIR/"staticfiles")

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config("DBNAME"),
        'USER': config("DBUSER"),
        'PASSWORD': config("DBPASS"),
        'HOST': config("DBHOST"),
        'PORT': "",
    }
}

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
# import dj_database_url
# db_from_env = dj_database_url.config(conn_max_age=600)
# DATABASES['default'].update(db_from_env)

COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False

