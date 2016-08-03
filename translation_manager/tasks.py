from django.core.management import call_command

from django_rq import job

from django.core.cache import cache


@job
def makemessages_task():
    if not cache.get('make_translations_running'):
        cache.set('make_translations_running', True)
        call_command('makemessages')
        cache.delete('make_translations_running')
