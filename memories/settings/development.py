from .base import *
import os
SECRET_KEY = config("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# MEDIA_URL = "/media/"
# MEDIA_ROOT = (BASE_DIR/"media")


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


CSRF_COOKIE_SECURE = True
CSRF_USE_SESSIONS = True

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)
COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = ["compressor.filters.cssmin.CSSMinFilter"]
COMPRESS_JS_FILTERS = ["compressor.filters.jsmin.JSMinFilter"]

# RECAPTCHA
RECAPTCHA_PUBLIC_KEY = config("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = config("RECAPTCHA_PRIVATE_KEY")

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_PORT=587
DEFAULT_FROM_EMAIL="Memories"

DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
DROPBOX_OAUTH2_TOKEN = config("DROPBOX_OAUTH2_TOKEN")


MEDIA_URL = '/memoriesMe/media/' 
DROPBOX_ROOT_PATH = MEDIA_URL
MEDIA_ROOT = (BASE_DIR/'media')

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

# import dj_database_url
# db_from_env = dj_database_url.config(conn_max_age=600)
# DATABASES['default'].update(db_from_env)
