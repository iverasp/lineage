import os
import ldap

DEBUG = False
TEMPLATE_DEBUG = DEBUG

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_SETTINGS_DIRECTORY = os.path.dirname(globals()['__file__'])
PROJECT_ROOT_DIRECTORY = os.path.join(PROJECT_SETTINGS_DIRECTORY, '..')


DATABASE_ROUTERS = ['ldapdb.router.Router']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Oslo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'some_random_secret_key'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
)

TEMPLATE_CONTEXT_LOADERS = (
    'django.core.context_processors.static',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'lineage.urls'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT_DIRECTORY, 'collected_static')

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'ldapdb',
    'apps.ldap_manager',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django_tables2',
    'bootstrap3',
    'tastypie',
    'django_password_strength',
)

LOGIN_URL = '/admin'

DEFAULT_SHELLS = (
    ('/bin/false', 'false'),
    ('/bin/bash', 'bash'),
)

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

DATE_INPUT_FORMATS = ['%Y-%m-%d',      # '2006-10-25'
                      '%m/%d/%Y',       # '10/25/2006'
                      '%m/%d/%y']

try:
    from local_settings import *
    SHELLS = DEFAULT_SHELLS + ADDITIONAL_SHELLS
    print(BASE_DN)
except ImportError as e:
    print(e)
    SHELLS = DEFAULT_SHELLS
    pass
