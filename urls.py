from django.contrib import admin
from django.urls import include, re_path
from translation_manager import urls as translation_urls


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^django-rq/', include('django_rq.urls')),
    re_path(r'^translations/', include(translation_urls))
]
