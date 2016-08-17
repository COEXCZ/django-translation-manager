from django.contrib import admin
from django.conf.urls import patterns, url, include

from translation_manager.settings import get_settings

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),

)

if get_settings('TRANSLATIONS_PROCESSING_METHOD') == 'async_django_rq':
    urlpatterns += (url(r'^django-rq/', include('django_rq.urls')),)
