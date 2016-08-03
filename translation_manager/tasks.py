from django.core.management import call_command

from django.core.cache import cache

def makemessages_task():
    call_command('makemessages')
    cache.delete('make_translations_running')
