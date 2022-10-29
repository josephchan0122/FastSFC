"""
Settings for Production Server
"""
from app.settings.base import *   # pylint: disable=W0614,W0401

DEBUG = False

SITE_HOST = 'http://fastsfc.com'

ADMINS = (
    ('FastSFC', 'hello@fastsfc.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fastsfc',
        'USER': 'fastdataco',
        'PASSWORD': 'Stayc00l1',
        'HOST': 'fastsfc.cxj2xwr2zi6a.ap-southeast-1.rds.amazonaws.com',
        'PORT': 3306,
    }
}

# ==============================================================================
# AWS access key
# ==============================================================================

AWS_S3_BUCKET = 'fastsfc'

# ==============================================================================
# ElasticSearch
# ==============================================================================

ES_HOST = 'https://4ff38a988809474b8016e6bb1c194473.ap-southeast-1.aws.found.io:9243'
ES_USER = 'elastic'
ES_USE_SSL = True
ES_PASSWORD = 'U5LnMoBB7RAidQrxsSEtY1BD'

# ==============================================================================
# Templates (use dist folder)
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
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

SITE_HOST = "http://fastsfc.com"
