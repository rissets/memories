from .base import *
import sys
# import django_heroku
import dj_database_url
from decouple import config

# django_heroku.settings(locals())
DEBUG = config("DEBUG_VALUE", "False") == "True"

ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", 'localhost,127.0.0.1').split(",")

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

DEVELOPMENT_MODE = config("DEVELOPMENT_MODE", "False") == "True"

if DEVELOPMENT_MODE is True:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    if config("DATABASE_URL", None) is None:
        raise Exception("DATABASE_URL environment variable not defined")
    DATABASES = {
        "default": dj_database_url.parse(os.environ.get("DATABASE_URL")),
    }
# import dj_database_url
# db_from_env = dj_database_url.config(conn_max_age=600)
# DATABASES['default'].update(db_from_env)

COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False

