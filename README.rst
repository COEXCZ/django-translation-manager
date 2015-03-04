######
README
######

Install package
===============

* use pip to get the package
  ::
      pip install git+git://github.com/COEXCZ/django-translation-manager.git

* add 'translation_manager' to settings.py: INSTALLED_APPS

* add variables from Translation Manager's defaults.py to your settings.py

* add post_save signal to restart server:
  ::
      from translation_manager.signals import post_save as translation_post_save
      
      translation_post_save.connect(restart_server, sender=None)


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

