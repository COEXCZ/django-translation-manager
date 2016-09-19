######
README
######


.. image:: https://travis-ci.org/COEXCZ/django-translation-manager.svg
   :target: https://travis-ci.org/COEXCZ/django-translation-manager
   :alt: Travis

.. image:: https://coveralls.io/repos/COEXCZ/django-translation-manager/badge.svg?branch=master
   :target: https://coveralls.io/github/COEXCZ/django-translation-manager?branch=master
   :alt: Coveralls

.. image:: https://landscape.io/github/COEXCZ/django-translation-manager/master/landscape.svg?style=flat
   :target: https://landscape.io/github/COEXCZ/django-translation-manager/master
   :alt: Code Health

.. image:: https://img.shields.io/pypi/v/django-translation-manager.svg
   :target: https://pypi.python.org/pypi/django-translation-manager/
   :alt: PYPI

.. image:: https://readthedocs.org/projects/django-translation-manager/badge/?version=master
   :target: http://django-translation-manager.readthedocs.org/en/master/
   :alt: Read the docs

.. image:: https://requires.io/github/COEXCZ/django-translation-manager/requirements.svg?branch=master
     :target: https://requires.io/github/COEXCZ/django-translation-manager/requirements/?branch=master
     :alt: Requirements Status

Install package
===============

* use pip to get the package
  ::
      pip install django-translation-manager

* add 'translation_manager' to settings.py: INSTALLED_APPS

* add variables from Translation Manager's defaults.py to your settings.py

* add post_save signal to restart webserver:
  ::
      from translation_manager.signals import post_save as translation_post_save
      
      translation_post_save.connect(restart_server, sender=None)


Supported versions of django
============================

We support all django versions greater or equal 1.8.


Using with django-rq
====================

We support asynchronous translation processing by django-rq.

Set translation processing method in settings.py
::
    TRANSLATIONS_PROCESSING_METHOD = 'async_django_rq'

Inslall django-rq
::
    pip install django_rq

Install django-redis-cache
::
    pip install django-redis-cache

We tested it with django-rq 0.9.1 and django-redis-cache 1.6.5

For configuration django_rq see  https://github.com/ui/django-rq


SyncDB
======
use syncdb
::
    ./manage.py syncdb

or migrate:
::
    ./manage.py migrate


Load strings from po files
==========================
via python shell
::
    ./manage.py shell
    
    from translation_manager.manager import Manager
    
    m = Manager()
    m.load_data_from_po()
    

Add link to translation admin
=============================

this is optional in case you need it
::
    {% url admin:translation_manager_translationentry_changelist %}


Known bugs
==========

If you are using different base site you have to register admin to your site.


License note
============

Django Translation Manager is available under Mozilla Public License 2.0

http://choosealicense.com/licenses/mpl-2.0/

Donate
======

.. image:: https://img.shields.io/badge/paypal-donate-yellow.svg
   :target: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=PUQZRR48HXXDC



Thank you!
----------

We really appreciate every donation that helps us take Django Translation Manager to the next level.
