"""
WSGI config for risset project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
# from whitenoise import WhiteNoise

from django.core.wsgi import get_wsgi_application

settings_module = 'memories.settings.production' if 'WEBSITE_HOSTNAME' in os.environ else 'memories.settings.development'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
# application = WhiteNoise(application)

