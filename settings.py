# Initialize App Engine and import the default settings (DB backend, etc.).
# If you want to use a different backend you have to remove all occurences
# of "djangoappengine" from this file.
from djangoappengine.settings_base import *

import os
ROOT_PATH = os.path.dirname(__file__)


# Activate django-dbindexer for the default database
DATABASES['native'] = DATABASES['default']
DATABASES['default'] = {'ENGINE': 'dbindexer', 'TARGET': 'native'}
AUTOLOAD_SITECONF = 'indexes'

SECRET_KEY = '=r-$b*8hglm+858&9t043hlm6-&6-3d3vfc4((7yd0dbrakhvi'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'registration',
    'autoload',
    'dbindexer',
    'about',
    'ideas',
    'bootstrap_toolkit',
    'contactus',
    'tastypie',
    'djangotoolbox',

    # djangoappengine should come last, so it can override a few manage.py commands
    'djangoappengine',
)

MIDDLEWARE_CLASSES = (
    # This loads the index definitions, so it has to come first
    'autoload.middleware.AutoloadMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
)

# This test runner captures stdout and associates tracebacks with their
# corresponding output. Helps a lot with print-debugging.
TEST_RUNNER = 'djangotoolbox.test.CapturingTestSuiteRunner'

# For mail
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'limeblaststudios'
EMAIL_HOST_PASSWORD = 'RussianPussy'
EMAIL_PORT = 587

# For registration app
ACCOUNT_ACTIVATION_DAYS = 7 
DEFAULT_FROM_EMAIL = 'limeblaststudios@gmail.com'
SERVER_EMAIL = 'limeblaststudios@gmail.com'

# For the static files
STATIC_ROOT = "static"
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(ROOT_PATH, 'media')
MEDIA_URL = '/media/'


LOGIN_REDIRECT_URL = '/'

ADMIN_MEDIA_PREFIX = '/media/admin/'
TEMPLATE_DIRS = (os.path.join(ROOT_PATH, 'templates'),)

ROOT_URLCONF = 'urls'


# For Production
# Comment out for debug
#EMAIL_BACKEND = 'appengine_emailbackend.EmailBackend'
EMAIL_BACKEND = 'appengine_emailbackend.async.EmailBackend'

#DEBUG = TEMPLATE_DEBUG = False

ADMINS = (
    ('Laimonas Turauskas', 'laimiux@gmail.com'),
)
