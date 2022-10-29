"""
Sample Settings for Local Development (save your own as local.py in this folder)
"""
from app.settings.base import *   # noqa: F401

DEBUG = True

SITE_HOST = 'http://localhost:8000'

ADMINS = (
    ('justin', 'justinyek@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',   # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'fastsfc',                      # Or path to database file if using sqlite3.
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',                    # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                             # Set to empty string for default.
    }
}

# ROOT_URLCONF = '{{ project_name }}.urls.local'
# WSGI_APPLICATION = '{{ project_name }}.wsgi.local.application'
