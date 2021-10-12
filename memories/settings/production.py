from .base import *
import django_heroku
import dj_database_url
django_heroku.settings(locals())
DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'memoriesrisset.herokuapp.com', 'memories.risset.me' ]

PRODUCTION_APPS = ['whitenoise.runserver_nostatic']

DEVELOPMENT_MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

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

