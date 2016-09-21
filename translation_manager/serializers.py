from .settings import get_settings

if get_settings('TRANSLATION_ENABLE_API_COMMUNICATION'):
    from rest_framework import serializers
    from translation_manager.models import TranslationEntry


    class TranslationSerializer(serializers.ModelSerializer):
        class Meta:
            model = TranslationEntry
            fields = ('original', 'translation')
