from .settings import get_settings
from django.urls import re_path, include

from .views import SyncView

urlpatterns = [
    re_path(r'^sync/$', SyncView.as_view(), name='sync'),
]

if get_settings('TRANSLATIONS_PROCESSING_METHOD') == 'async_django_rq':
    urlpatterns.append(
        re_path(r'^django-rq/', include('django_rq.urls'))
    )

if get_settings('TRANSLATIONS_ENABLE_API_COMMUNICATION'):
    from translation_manager import views

    urlpatterns.append(
        re_path(r'^(?P<language>[\w-]+)/$', views.TranslationListView.as_view(), name='translations'),
    )
