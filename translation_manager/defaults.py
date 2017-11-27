"""
Settings required in you project settings.
Please modify according to your requirements.
Usage can be found in example project.
"""

# Required paths to all locale dirs
# LOCALE_PATHS = [
#     '/foo/bar/locale',
#     '/foo/foo/bar/locale',
# ]
LOCALE_PATHS = []

# Path to project basedir / workdir - root folder of project
# TRANSLATIONS_BASE_DIR = '/foo/bar'
TRANSLATIONS_BASE_DIR = ''

# Path to project sorce code files, usually BASE_DIR
TRANSLATIONS_PROJECT_BASE_DIR = ''

# Mode the translation manager behaves when creating
# translations mainly from multiple locale files
# Default value is N, where translation in DB are
# only once for specific locale file.
# Another option is P, where is translation manager
# promiscuous and creates for every translation it's
# instance for every locale file. It's useful, i.e.
# if you want has original system trasnlations and
# also client's custom translations

TRANSLATIONS_MODE = "N"

# For storing all translations to db regardless they have
# any occurrencies or not set True, otherwise set False.
# If False only translations having occurrencies in your
# application will be stored.
TRANSLATIONS_ALLOW_NO_OCCURRENCES = False

# Dirs and files ignored for makemessages.
# TRANSLATIONS_IGNORED_PATHS = ['env', 'foo', 'bar']
TRANSLATIONS_IGNORED_PATHS = ['env']

# Backup on makemessages:
TRANSLATIONS_MAKE_BACKUPS = True

# Clean .po files (delete content) after backup (this prevents duplicities)
TRANSLATIONS_CLEAN_PO_AFTER_BACKUP = True

# Forced filters on changelist queryset.
# Uses ORed original__contains Django ORM filter.
# TRANSLATIONS_QUERYSET_FORCE_FILTERS = ['foo', 'bar']
TRANSLATIONS_QUERYSET_FORCE_FILTERS = []

# Language to display in hint column to help translators
# see translation of string in another language
# TRANSLATIONS_HINT_LANGUAGE = 'foo'
TRANSLATIONS_HINT_LANGUAGE = ''

# Relative path to locale dir with hint languages
# Current locale path of translated string used by default
TRANSLATIONS_HINT_LANGUAGE_FORCED_RELATIVE_LOCALE_PATH = ''

# exclude fields from administration:
TRANSLATIONS_ADMIN_EXCLUDE_FIELDS = []

# Define admin fields manually: for all fields look to admin.py:default_fields
TRANSLATIONS_ADMIN_FIELDS = []

# Label of custom filters
TRANSLATIONS_CUSTOM_FILTERS_LABEL = ""

# List containing regex expression and label used for filtering in administration.
# Each object should be a tuple of (regex_filter, label)
TRANSLATIONS_CUSTOM_FILTERS = []

# Limits locale paths of published translations when updating POs from DB.
TRANSLATIONS_UPDATE_FORCED_LOCALE_PATHS = []

# List of django domains for translation strings.
# Defaults are ['django', 'djangojs']
TRANSLATIONS_DOMAINS = ['django', 'djangojs']

# auto create directories by translation languages
TRANSLATIONS_AUTO_CREATE_LANGUAGE_DIRS = True

# Type of translation computation running mode.
# For synchronous type 'sync' (default)
# For asynchronous type 'async_django_rq with django_rq usage
TRANSLATIONS_PROCESSING_METHOD = 'sync'

# Name of rq_queue, default is 'default'
TRANSLATIONS_PROCESSING_QUEUE = 'default'

# Enable export translations from .po files in json obects via django REST Framework
TRANSLATIONS_ENABLE_API_COMMUNICATION = False

# Enable searching in Angular js source codes for translation strings
TRANSLATIONS_ENABLE_API_ANGULAR_JS = False

# Settings below only works if TRANSLATIONS_ENABLE_API_COMMUNICATION is enabled

# Absolute path to client api application source codes
# Source codes must be on a same filesystem as current app
TRANSLATIONS_API_CLIENT_APP_SRC_PATH = ''

# Regex for matching translation strings in clint src files
TRANSLATIONS_API_TRANSLATION_STRINGS_REGEX = ''

TRANSLATIONS_API_TRANSLATION_STRINGS_REGEX_LIST = []

# Dirs and files ignored for makemessages in client api app.
TRANSLATIONS_API_IGNORED_PATHS = []

# Similar as for base use above.
# For api client app translation strings
TRANSLATIONS_API_QUERYSET_FORCE_FILTERS = []

# If True, api returns all translations, it does not matter if it is filled with value translation
TRANSLATIONS_API_RETURN_ALL = True

# Permission classes for translation manager api methods.
# If empty, no permission is provided
TRANSLATIONS_API_PERMISSION_CLASSES = ()

# Authentication classes for translation manager api methods.
# If empty, no authentication is provided
TRANSLATIONS_API_AUTHENTICATION_CLASSES = ()

# Local token, have to be present as TRANSLATIONS_SYNC_REMOTE_TOKEN on target env
TRANSLATIONS_SYNC_LOCAL_TOKEN = ''

# Remote URL of TRM which will be synced to local TRM
TRANSLATIONS_SYNC_REMOTE_URL = ''

# Remote token, which is set as TRANSLATIONS_SYNC_LOCAL_TOKEN on remote site
TRANSLATIONS_SYNC_REMOTE_TOKEN = ''

# Basic Auth user for remote authentication
TRANSLATIONS_SYNC_REMOTE_USER = None

# Basic Auth password for remote authentication
TRANSLATIONS_SYNC_REMOTE_PASSWORD = None

# Useful when remote url does have any issue with SSL certificate
# Applied when requests.get(<url>, verify=<TRANSLATIONS_SYNC_VERIFY_SSL>) is called
TRANSLATIONS_SYNC_VERIFY_SSL = True
