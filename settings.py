"""
Django settings for project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
import os
import sys

from translation_manager.settings import get_settings

from django.utils.translation import gettext_lazy as _

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b=@ru#--%)2v%fx-zbhdfxnv#o8bjn7d-kjp(zc0r@1z_lh#3*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'translation_manager',
    'django_rq',
    'rest_framework'
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'testdb',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('cs', _('Czech')),
    ('en', _('English')),
)

TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'translation_manager', 'templates')
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

TESTING = sys.argv[1:2] == ['test']

if TESTING:
    LOCALE_PATHS = [os.path.join(BASE_DIR, 'tests', "locale")]
    TRANSLATIONS_BASE_DIR = BASE_DIR
else:
    LOCALE_PATHS = [
        os.path.join(BASE_DIR, 'translation_manager', 'locale')
    ]
    TRANSLATIONS_BASE_DIR = os.path.join(BASE_DIR, 'translation_manager')

TRANSLATIONS_MODE = "N"

TRANSLATIONS_PROJECT_BASE_DIR = BASE_DIR

TRANSLATIONS_ALLOW_NO_OCCURRENCES = False

TRANSLATIONS_IGNORED_PATHS = ['env']

TRANSLATIONS_MAKE_BACKUPS = True
TRANSLATIONS_CLEAN_PO_AFTER_BACKUP = False
TRANSLATIONS_QUERYSET_FORCE_FILTERS = []

TRANSLATIONS_HINT_LANGUAGE = 'en'

# e.g. 'occurrences', 'locale_parent_dir', 'domain'
TRANSLATIONS_ADMIN_EXCLUDE_FIELDS = []

TRANSLATIONS_ADMIN_FIELDS = []

TRANSLATIONS_CUSTOM_FILTERS = (
    (r'^admin-', 'Admin fields'),
    (r'^test-', 'Test fields'),
)

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'localhost:6379',
    },
}

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'PASSWORD': '',
        'DEFAULT_TIMEOUT': 360,
        'USE_REDIS_CACHE': 'default',
    }
}

# enable export translations from .po files in json obects via django REST Framework
TRANSLATIONS_ENABLE_API_COMMUNICATION = True

# settings below only works if TRANSLATIONS_ENABLE_API_COMMUNICATION is enabled

# absolute path to client api application source codes
# source codes must be on a same filesystem as current app
TRANSLATIONS_API_CLIENT_APP_SRC_PATH = ''

TRANSLATIONS_ENABLE_API_ANGULAR_JS = True

TRANSLATIONS_API_TRANSLATION_STRINGS_REGEX_LIST = [r'\{\{\s*\\[\'\"]\s*([a-z0-9\-\_]*)s*\\[\'\"]\s*\|\s*translate\s*\}\}',]

# Dirs and files ignored for makemessages in client api app.
TRANSLATIONS_API_IGNORED_PATHS = ['front-']

TRANSLATIONS_API_RETURN_ALL = False

TRANSLATIONS_SYNC_REMOTE_URL = 'http://localhost/translations/sync/'
TRANSLATIONS_SYNC_REMOTE_TOKEN = '1234abcd'
TRANSLATIONS_SYNC_LOCAL_TOKEN = '1234abcd'
TRANSLATIONS_SYNC_REMOTE_USER = None
TRANSLATIONS_SYNC_REMOTE_PASSWORD = None


try:
    from settings_local import *
except ImportError:
    pass
