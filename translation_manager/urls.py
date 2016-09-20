from settings import get_settings
from django.conf.urls import url

if get_settings('TRANSLATION_ENABLE_API_COMMUNICATION'):
    from translation_manager import views

    urlpatterns = [
        url(r'^(?P<language>[\w-]+)/$', views.TranslationListView.as_view(), name='translations'),
    ]
