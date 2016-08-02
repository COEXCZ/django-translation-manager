from django.contrib import admin

try:
    from django.conf.urls import patterns, url, include
except ImportError:
    # Old django fix
    from django.conf.urls.defaults import patterns, url, include
    admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^django-rq/', include('django_rq.urls'))
)
