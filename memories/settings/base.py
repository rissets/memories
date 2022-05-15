import os
from pathlib import Path

from blog.utils import user_directory_path
from django.utils.translation import gettext_lazy as _

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
APP_DIR = Path(__file__).resolve().parent
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'static', 'serviceworker.js')


# SECURITY WARNING: keep the secret key used in production secret!

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
]

MY_APPS = [
    'blog',
]

THIRD_PARTY_APPS = [
    # blog dependent
    'sorl.thumbnail',
    'taggit',
    'admin_honeypot',
    'ckeditor',
    'mptt',
    'pwa',
    'accounts',
    'django_extensions',
    'newsletter',
    # 'storages',
    
    "whitenoise.runserver_nostatic",

    # portfolio dependent
    'compressor',
    'meta',
    'modeltranslation',
    'captcha'
]

PRODUCTION_APPS = []

INSTALLED_APPS = DJANGO_APPS + MY_APPS + THIRD_PARTY_APPS + PRODUCTION_APPS

SITE_ID = 1

BUILT_IN_MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

THIRD_PARTY_MIDDLEWARE = [
    
]
DEVELOPMENT_MIDDLEWARE = []

MIDDLEWARE = BUILT_IN_MIDDLEWARE + THIRD_PARTY_MIDDLEWARE + DEVELOPMENT_MIDDLEWARE

ROOT_URLCONF = 'memories.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.i18n',
                'blog.views.categories',
            ],
        },
    },
]

WSGI_APPLICATION = 'memories.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {
            'user_attributes': (
                'username', 'email', 'first_name', 'last_name'
            ),
            'max_similarity': 0.5
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 5,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
# LANGUAGE_CODE = 'id'

# STORAGES

STATICFILES_DIRS = [BASE_DIR/"static"]
STATIC_URL = "/static/"


LOCALE_PATHS = (BASE_DIR / 'locale',)

LANGUAGES = (
    ('id', _('Indonesian')),
    ('en', _('English')),
)

DEFAULT_LANGUAGE = 'id'
MODELTRANSLATION_DEFAULT_LANGUAGE = 'id'

MODELTRANSLATION_LANGUAGES = ('id', 'en')

MODELTRANSLATION_PREPOPULATE_LANGUAGE = 'id'

MODELTRANSLATION_FALLBACK_LANGUAGES = ('id', 'en')

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/






# MEDIA_ROOT = DROPBOX_ROOT_PATH
# MEDIA_URL = "/media/"
# MEDIA_ROOT = (BASE_DIR/'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CKEDITOR
CKEDITOR_UPLOAD_PATH = 'posts/ckeditor/'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'heigth': '100hv',
        'width': '100%',
        'toolbar_Custom': [
            ['Styles', 'Format', 'Bold', 'Italic', 'Underline',
                'Strike', 'SpellChecker', 'Undo', 'Redo'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flash', 'Table', 'HorizontalRule'],
            ['TextColor', 'BgColor'],
            ['Smiley', 'SpecialChar'], ['Source']
        ],
        'toolbar': 'Special',
        'tollbar_Special': [
            ['CodeSnippet'],
        ],
        'extraPlugins': ',' .join(['codesnippet']),
    }
}


# PWA
# PWA_APP_DEBUG_MODE = False
PWA_APP_NAME = 'Memories'
PWA_APP_DESCRIPTION = _(
    "Get information that is informative, motivating and in accordance with facts. Protect yourself from fraud, and be someone who is open minded.")
PWA_APP_THEME_COLOR = '#2E2E2E'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        'src': '/static/blog/assets/img/icon-app.png',
        'sizes': '240x240'
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/blog/assets/img/icon-apple.png',
        'sizes': '160x160'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/blog/assets/img/splash.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'id'


# LOGIN

LOGIN_REDIRECT_URL = 'accounts:profile'
LOGIN_URL = 'accounts:sign-in'
LOGOUT_REDIRECT_URL = 'accounts:sign-out'

# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# NEWSLETTER
NEWSLETTER_CONFIRM_EMAIL = True
NEWSLETTER_CONFIRM_EMAIL_UNSUBSCRIBE = True
NEWSLETTER_CONFIRM_EMAIL_UPDATE = True
NEWSLETTER_RICHTEXT_WIDGET = "ckeditor.widgets.CKEditorWidget"
NEWSLETTER_THUMBNAIL = 'sorl-thumbnail'

# Amount of seconds to wait between each email. Here 100ms is used.
NEWSLETTER_EMAIL_DELAY = 0.1


# META
META_SITE_PROTOCOL = 'https'
META_INCLUDE_KEYWORDS = ['danang haris setiawan', 'portfolio', 'journal', 'wiki engineering']
META_DEFAULT_KEYWORDS = ['danang haris setiawan', 'portfolio', 'journal']
META_SITE_DOMAIN = 'localhost'
META_USE_SITES = False
