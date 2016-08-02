from django.core.management import call_command

from django_rq import job

from django.core.cache import cache


@job
def makemessages_task():
    if not cache.get('Translation_computation_running'):
        cache.set('Translation_computation_running', True)
        call_command('makemessages')
        cache.delete('Translation_computation_running')
