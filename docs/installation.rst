.. _installation:

Installation
============

.. _download-installation:

Download / Installation
-----------------------

The easiest way to get and install Django Translation Manager is via pip,
feel free to omit the first two lines if you don't want to use virtualenv

.. code-block:: console

    virtualenv env --no-site-packages
    source env/bin/activate
    pip install django-translation-manager

In case you are curious about the source, willing to contribute, or you just want
to do it yourself, feel free to see our GitHub `project page`_

.. _project page: https://github.com/COEXCZ/django-translation-manager/

After you have installed the package, it's time for configuration

Configuratuion
--------------

1) First, add translation_manager to INSTALLED_APPS to your project's settings in *settings.py*.
  We're calling our project *project* for example's sake

  .. code-block:: python

      INSTALLED_APPS = (
          'django.contrib.admin',
          'django.contrib.auth',
          # ...
          # this is what we have added:
          'translation_manager',
      )

2) Next, add the following variables to your settings and set them accordingly

  .. code-block:: python

      # Required paths to all locale dirs
      LOCALE_PATHS = []

      # Path to project basedir / workdir - root folder of project
      # TRANSLATIONS_BASE_DIR = os.path.dirname(os.path.dirname(__file__))
      TRANSLATIONS_BASE_DIR = ''

      # Language to display in hint column to help translators
      # see translation of string in another language
      TRANSLATIONS_HINT_LANGUAGE = ''


3) add post_publish signal to restart the server:

  .. code-block:: python

      from translation_manager.signals import post_publish as translation_post_publish

      translation_post_publish.connect(restart_server, sender=None)


4) use syncdb or migrate

  .. code-block:: console

      ./manage.py syncdb
      ./manage.py migrate


5) Now load strings from .po files via python shell

  .. code-block:: console

      ./manage.py shell

  .. code-block:: python

      from translation_manager.manager import Manager

      m = Manager()
      m.load_data_from_po()

6) if you need, add a link to translation admin

  .. code-block:: python

      {% url admin:translation_manager_translationentry_changelist %}

You should now have your Django Translation Manager up and running
