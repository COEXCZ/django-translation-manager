from django.test import override_settings
from rest_framework.test import APITestCase

from translation_manager.models import TranslationEntry
from translation_manager import defaults


@override_settings(TRANSLATIONS_ENABLE_API_COMMUNICATION=True)
class TranslationTests(APITestCase):

    def setUp(self):
        TranslationEntry.objects.create(language='cs', original='admin-test', translation='test in admin',
                                        is_published=True)
        TranslationEntry.objects.create(language='cs', original='test', translation='other test', is_published=True)

    def test_get_translations(self):
        defaults.TRANSLATIONS_API_QUERYSET_FORCE_FILTERS = []
        response = self.client.get('/translations/cs/')
        self.assertTrue(len(response.data) == 2)

    def test_force_filter(self):
        defaults.TRANSLATIONS_API_QUERYSET_FORCE_FILTERS = ['admin-']
        response = self.client.get('/translations/cs/')
        self.assertTrue(len(response.data) == 1)
