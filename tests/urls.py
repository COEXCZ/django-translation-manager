from django.contrib import admin
from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
)
