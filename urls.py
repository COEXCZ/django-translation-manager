from django.contrib import admin
from django.conf.urls import url, include
from translation_manager import urls as translation_urls

from translation_manager.settings import get_settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^django-rq/', include('django_rq.urls')),
    url(r'^translations/', include(translation_urls))
]
