README
======

# 1) install package 

pip install -e git+git@bitbucket.org:coex/translation_manager.git#egg=translation_manager

add 'translation_manager' to settings.py: INSTALLED_APPS

add variables from https://bitbucket.org/coex/translation_manager/src/master/translation_manager/app.settings.py?at=master to settings.py

add post_save signal to restart server:


```python
from translation_manager.signals import post_save as translation_post_save

translation_post_save.connect(restart_server, sender=None)

```

# 2) syncdb 

./manage.py syncdb

or migrate:

./manage.py migrate


# 3) load strings from po files

./manage.py shell

```python
from translation_manager.manager import Manager

m = Manager()
m.load_data_from_po()

```

# 4) optional: add link to translation admin

{% url admin:translation_manager_translationentry_changelist %}


Known bugs:
----------

If you are using different base site you have to register admin to your site.


License note:


Commercial license is being prepared. Please contact us for details at info@coex.cz.
