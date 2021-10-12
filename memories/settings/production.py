from .base import *

DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'memoriesrisset.herokuapp.com']

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'risset',
#         'USER': 'rissetuser',
#         'PASSWORD': config('PASSWORD_DB'),
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False
