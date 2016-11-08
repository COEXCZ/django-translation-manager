from .settings import get_settings

if get_settings('TRANSLATIONS_ENABLE_API_COMMUNICATION'):
    from rest_framework import serializers
    from translation_manager.models import TranslationEntry


    class TranslationSerializer(serializers.ModelSerializer):

        class Meta:
            model = TranslationEntry
            fields = ('original', 'translation')

        def to_representation(self, obj):
            return {
                obj.original: obj.translation
            }
