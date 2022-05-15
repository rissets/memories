#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from dotenv import load_dotenv

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f"Set the {var_name} environment variable."
        raise ImproperlyConfigured(error_msg)


def main():
    """Run administrative tasks."""
    
    if not 'WEBSITE_HOSTNAME' in os.environ:
        print("Loading environment variables for .env file")
        load_dotenv('./.env')
        settings_module = "memories.settings.development"
    else:
        settings_module = "memories.settings.production" 
    # When running on Azure App Service you should use the production settings.
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
        
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
