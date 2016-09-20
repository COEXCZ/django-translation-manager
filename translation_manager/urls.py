from settings import get_settings
from django.conf.urls import url, include

urlpatterns = []

if get_settings('TRANSLATIONS_PROCESSING_METHOD') == 'async_django_rq':
    urlpatterns.append(
        url(r'^django-rq/', include('django_rq.urls'))
    )

if get_settings('TRANSLATION_ENABLE_API_COMMUNICATION'):
    from translation_manager import views

    urlpatterns.append(
        url(r'^(?P<language>[\w-]+)/$', views.TranslationListView.as_view(), name='translations'),
    )
