.. _configuration:

Configuration
=============

You can configure Django Translation Manager by overriding it's default settings in your settings.py
Default settings can be found in defaults.py in django translation manager folder.


Mandatory parameters
--------------------

Those have to be explicitly set for Django Transaltion Manager to work

.. code-block:: python

    # Required paths to all locale dirs
    # LOCALE_PATHS = [
    #     '/foo/bar/locale',
    #     '/foo/foo/bar/locale',
    # ]
    LOCALE_PATHS = []

.. code-block:: python

    # Path to project basedir / workdir - root folder of project
    # TRANSLATIONS_BASE_DIR = '/foo/bar'
    TRANSLATIONS_BASE_DIR = ''

.. code-block:: python

    # Language to display in hint column to help translators
    # see translation of string in another language
    # TRANSLATIONS_HINT_LANGUAGE = 'foo'
    TRANSLATIONS_HINT_LANGUAGE = ''


Optional parameters
-------------------


.. code-block:: python

    # Mode the translation manager behaves when creating
    # translations mainly from multiple locale files
    # Default value is N, where translation in DB are
    # only once for specific locale file.
    # Another option is P, where is translation manager
    # promiscuous and creates for every translation it's
    # instance for every locale file. It's useful, i.e.
    # if you want has original system translations and
    # also client's custom translations

    TRANSLATIONS_MODE = "N"

.. code-block:: python

    # For storing all translations to db regardless they have
    # any occurrences or not set True, otherwise set False.
    # If False only translations having occurrences in your
    # application will be stored.
    TRANSLATIONS_ALLOW_NO_OCCURRENCES = False

.. code-block:: python

    # Dirs and files ignored for makemessages.
    # TRANSLATIONS_IGNORED_PATHS = ['env', 'foo', 'bar']
    TRANSLATIONS_IGNORED_PATHS = ['env']

.. code-block:: python

    # Backup on make messages:
    TRANSLATIONS_MAKE_BACKUPS = True

.. code-block:: python

    # Clean .po files (delete content) after backup (this prevents duplicities)
    TRANSLATIONS_CLEAN_PO_AFTER_BACKUP = True


.. code-block:: python

    # Forced filters on changelist queryset.
    # Uses ORed original__contains Django ORM filter.
    # TRANSLATIONS_QUERYSET_FORCE_FILTERS = ['foo', 'bar']
    TRANSLATIONS_QUERYSET_FORCE_FILTERS = []


.. code-block:: python

    # Relative path to locale dir with hint languages
    # Current locale path of translated string used by default
    TRANSLATIONS_HINT_LANGUAGE_FORCED_RELATIVE_LOCALE_PATH = ''


.. code-block:: python

    # exclude fields from administration:
    TRANSLATIONS_ADMIN_EXCLUDE_FIELDS = []


.. code-block:: python

    # define admin fields manually: for all fields look to admin.py:default_fields
    TRANSLATIONS_ADMIN_FIELDS = []


.. code-block:: python

    # tuple of title and list of regex expression used for filtering in administration.
    # Each object should be a tuple of (regex_filter, label)
    TRANSLATIONS_CUSTOM_FILTERS = []

