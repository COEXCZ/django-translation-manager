from django.core.management import call_command

from django.core.cache import cache

from .settings import get_settings

if get_settings('TRANSLATIONS_PROCESSING_METHOD') == 'async_django_rq':

    from django_rq import job


    @job(get_settings('TRANSLATIONS_PROCESSING_QUEUE'))
    def makemessages_task():
        call_command('makemessages')
        cache.delete('make_translations_running')
else:
    def makemessages_task():
        call_command('makemessages')
        cache.delete('make_translations_running')
