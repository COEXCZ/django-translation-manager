.. _django_rq:

Using with django_rq
====================

If your application contains thousands of translation strings may be 
usefull to run actualization of translation strings in system as asynchronous task.
We support this feature via django_rq library.

Set 'async_django_rq' as translation processing method

.. code-block:: python

    TRANSLATIONS_PROCESSING_METHOD = 'async_django_rq'

We also considering to implement support for django-celery later

Set name of your django_rq quequ designated for django-translation-manager purposes

.. code-block:: python

    # TRANSLATIONS_PROCESSING_QUEUE = 'default'
    TRANSLATIONS_PROCESSING_QUEUE = ''

For configuration your django_rq queues see https://github.com/ui/django-rq

Finally you will need to install django_rq and django-redis-cache via pip

.. code-block:: python

    pip install django_rq
    pip install django-redis-cache
    
Testing took place in versions django-rq 0.9.1 and django-redis-cache 1.6.5
