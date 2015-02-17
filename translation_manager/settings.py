from django.conf import settings
from . import defaults


def get_settings(setting):
    """
    Looks for settings in django settings or in translation_manager.defaults
    """
    return getattr(settings, setting, getattr(defaults, setting))

