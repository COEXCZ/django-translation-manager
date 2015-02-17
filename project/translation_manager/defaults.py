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

# define admin fields manually: for all fields look to admin.py:default_fields
TRANSLATIONS_ADMIN_FIELDS = []

# tuple of title and list of regex expression used for filtering in administration. Each object should be a tuple of (regex_filter, label)
TRANSLATIONS_CUSTOM_FILTERS = []
