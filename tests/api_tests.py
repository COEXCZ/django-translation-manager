from translation_manager.settings import get_settings

if get_settings('TRANSLATION_ENABLE_API_COMMUNICATION'):
    from rest_framework.test import APITestCase
    from translation_manager.models import TranslationEntry
    from translation_manager import defaults


    class TranslationTests(APITestCase):
        def setUp(self):
            TranslationEntry.objects.create(language='cs', original='admin-test', is_published=True)
            TranslationEntry.objects.create(language='cs', original='test', is_published=True)

        def test_get_translations(self):
            defaults.TRANSLATIONS_API_QUERYSET_FORCE_FILTERS = []
            response = self.client.get('/translations/cs/')
            self.assertTrue(len(response.data) == 2)

        def test_force_filter(self):
            defaults.TRANSLATIONS_API_QUERYSET_FORCE_FILTERS = ['admin-']
            response = self.client.get('/translations/cs/')
            self.assertTrue(len(response.data) == 1)
