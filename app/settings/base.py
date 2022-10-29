import app as project_module
import sys
import os
"""Base settings shared by all environments"""
# Import global settings to make it easier to extend settings.
from django.conf.global_settings import *   # pylint: disable=W0614,W0401

# ==============================================================================
# Generic Django project settings
# ==============================================================================

DEBUG = True

SITE_ID = 1

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Asia/Singapore'
USE_TZ = True
USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', 'English'),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '&1tytok-=&lcy!iy-b#mzncwgksa3eux!un_$rk#1j^ssv3a3u'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'webpack_loader',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_ses',
    'django_filters',
    'compressor',
    'titlecase',
    'rest_framework',
    'jsonfield',
    'pandas',
    'elasticsearch_dsl',
    'certifi',
    'app.core',
    'app.log',
)

# ==============================================================================
# Calculation of directories relative to the project module location
# ==============================================================================


PROJECT_DIR = os.path.dirname(os.path.realpath(project_module.__file__))

PYTHON_BIN = os.path.dirname(sys.executable)
ve_path = os.path.dirname(os.path.dirname(os.path.dirname(PROJECT_DIR)))
# Assume that the presence of 'activate_this.py' in the python bin/
# directory means that we're running in a virtual environment.
if os.path.exists(os.path.join(PYTHON_BIN, 'activate_this.py')):
    # We're running with a virtualenv python executable.
    VAR_ROOT = os.path.join(os.path.dirname(PYTHON_BIN), 'var')
elif ve_path and os.path.exists(os.path.join(ve_path, 'bin',
                                             'activate_this.py')):
    # We're running in [virtualenv_root]/src/[project_name].
    VAR_ROOT = os.path.join(ve_path, 'var')
else:
    # Set the variable root to a path in the project which is
    # ignored by the repository.
    VAR_ROOT = os.path.join(PROJECT_DIR, 'var')

if not os.path.exists(VAR_ROOT):
    os.mkdir(VAR_ROOT)

# ==============================================================================
# Project URLS and media settings
# ==============================================================================

ROOT_URLCONF = 'app.urls'

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'

STATIC_URL = '/static/'
MEDIA_URL = '/uploads/'

STATIC_ROOT = os.path.join(VAR_ROOT, 'static')
MEDIA_ROOT = os.path.join(VAR_ROOT, 'uploads')

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
    os.path.join(PROJECT_DIR, '../.tmp'),
)

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': '',
        'STATS_FILE': os.path.join(PROJECT_DIR, '../webpack/webpack-stats.json'),
    }
}

# ==============================================================================
# Templates
# ==============================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ==============================================================================
# Middleware
# ==============================================================================

MIDDLEWARE_CLASSES += (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'app.core.middleware.xssharing.XsSharingMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

# ==============================================================================
# Rest framework
# ==============================================================================

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
}

# ==============================================================================
# Auth / security
# ==============================================================================

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

LOGIN_REDIRECT_URL = '/'

# ==============================================================================
# Miscellaneous project settings
# ==============================================================================

# For XSSharing middleware which allows cross domain XHR
XS_SHARING_ALLOWED_ORIGINS = '*'
ALLOWED_HOSTS = ['*']

# ==============================================================================
# AWS access key
# ==============================================================================

AWS_S3_BUCKET = 'fastsfc'
AWS_ACCESS_KEY_ID = 'AKIA5LXVWRAKCRZG7YFU'
AWS_SECRET_ACCESS_KEY = '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'

# ==============================================================================
# ElasticSearch
# ==============================================================================

ES_HOST = 'localhost'
ES_USER = 'elastic'
ES_USE_SSL = False
ES_PASSWORD = 'changeme'

# ==============================================================================
# Email (Django SES)
# ==============================================================================

EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_SES_REGION_NAME = 'us-west-2'
AWS_SES_REGION_ENDPOINT = 'email.us-west-2.amazonaws.com'
DEFAULT_FROM_EMAIL = 'FastSFC <hello@fastsfc.com>'
