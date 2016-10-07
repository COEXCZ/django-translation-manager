.. _angular_js:

Using with AngularJS
====================

We support translation of applications connected via Django REST framework

Initial support is primarily for framework AngularJs, but for example React is usefull too

Mandatory setting
-----------------

First step is to enable export translated strings via API

.. code-block:: python

    TRANSLATION_ENABLE_API_COMMUNICATION = True

Now you have to tell Django-translation-manager where are AngularJS source codes located

The important thing is that it must be in the same file system

.. code-block:: python

    # Enable searching in Angular js source codes for translation strings
    TRANSLATION_ENABLE_API_ANGULAR_JS = False

    # Absolute path to client api application source codes
    # TRANSLATION_API_CLIENT_APP_SRC_PATH = os.path.join(HOME_DIR, 'front')
    TRANSLATION_API_CLIENT_APP_SRC_PATH = ''

Last mandatory step is to tell Django-translation-manager how translation strings in AngularJS source codes looks like

.. code-block:: python

    # TRANSLATION_API_TRANSLATION_STRINGS_REGEX = r'\{\{\s*\\[\'\"]\s*([a-z0-9\-\_]*)s*\\[\'\"]\s*\|\s*translate\s*\}\}' 
    TRANSLATION_API_TRANSLATION_STRINGS_REGEX = r''

Optional settings
-----------------

You can ignore some roots in source code paths, for example static files

.. code-block:: python

    # TRANSLATION_API_IGNORED_PATHS = [
    #             'static',
    #             'media/js'
    # ]
    TRANSLATION_API_IGNORED_PATHS = []

You can specify prefix of translation strings provided via API

.. code-block:: python
 
    # TRANSLATIONS_API_QUERYSET_FORCE_FILTERS = [
    #             'front-',
    #             'system-'
    # ]
    TRANSLATIONS_API_QUERYSET_FORCE_FILTERS = []

.. code-block:: python

Further you can specify if API returns all translation strings for selected language or only translated
  
.. code-block:: python

    TRANSLATIONS_API_RETURN_ALL = False

At last you can assign permission and authentication classes for Django-translation-manager API method

.. code-block:: python

    # Permission classes for translation manager api methods.
    # If empty, no permission is provided
    TRANSLATION_API_PERMISSION_CLASSES = ()

    # Authentication classes for translation manager api methods.
    # If empty, no authentication is provided
    TRANSLATION_API_AUTHENTICATION_CLASSES = ()
