.. _installation:

Installation
============


install package
---------------

* use pip to get the package
  ::
      pip install git+git://github.com/COEXCZ/django-translation-manager.git

* add 'translation_manager' to settings.py: INSTALLED_APPS

* add variables from https://bitbucket.org/coex/translation_manager/src/master/translation_manager/app.settings.py?at=master to settings.py

* add post_save signal to restart server:
  ::
      from translation_manager.signals import post_save as translation_post_save

      translation_post_save.connect(restart_server, sender=None)


syncdb
------
use syncdb
::
    ./manage.py syncdb

or migrate:
::
    ./manage.py migrate


load strings from po files
--------------------------
via python shell
::
    ./manage.py shell

    from translation_manager.manager import Manager

    m = Manager()
    m.load_data_from_po()


add link to translation admin
-----------------------------

this is optional in case you need it
::
    {% url admin:translation_manager_translationentry_changelist %}



.. _download-installation:

Download / Installation
-----------------------

The easiest way to get and install Translation Manager is via pip,
feel free to omit the first two lines if you don't want to use virtualenv

.. code-block:: console

    virtualenv env --no-site-packages
    source env/bin/activate
    pip install git+git://github.com/COEXCZ/django-translation-manager.git

In case you are curious about the source, willing to contribute, or you just want
to do it yourself, feel free to see our GitHub `project page`_

.. _project page: https://github.com/COEXCZ/django-translation-manager/

Getting Started
---------------

After you have installed the package, it's time for configuration

First, add translation_manager to INSTALLED_APPS to your project's settings in *settings.py*.
We're calling our project *project* for example's sake

.. code-block:: python
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        # ...
        # this is what we have added:
        'project.translation_manager',
    )

Next, add the following variables to your settings and set them accordingly

.. code-block:: python
    # Required paths to all locale dirs
    LOCALE_PATHS = []

    # Path to project basedir / workdir - root folder of project
    # TRANSLATIONS_BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    TRANSLATIONS_BASE_DIR = ''

    # Language to display in hint column to help translators
    # see translation of string in another language
    TRANSLATIONS_HINT_LANGUAGE = ''


Displaying Errors
~~~~~~~~~~~~~~~~~

TODO


Next Steps
----------

TODO

The crash course has just skimmed the surface on how you can begin using
WTForms to handle form input and validation in your application. For more
information, you'll want to check the following:

 - The :ref:`WTForms documentation <doc-index>` has API documentation for the entire library.
 - :ref:`specific_problems` can help you tackle specific
   integration issues with WTForms and other frameworks.
 - The `mailing list`_ is where you can get help, discuss bugs in WTForms, and
   propose new features.

.. _mailing list: http://groups.google.com/group/wtforms/
