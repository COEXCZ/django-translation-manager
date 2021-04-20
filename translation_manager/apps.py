import os

from django.apps import AppConfig
from django.conf import settings


class TranslationManagerConfig(AppConfig):
    name = 'translation_manager'

    def ready(self):
        for path in settings.LOCALE_PATHS:
            os.makedirs(path, exist_ok=True)
