from django.test import TestCase
from django.contrib.auth.models import User

from translation_manager.manager import Manager as TranslationManager
from translation_manager.models import TranslationEntry


class TranslationCase(TestCase):
    def setUp(self):
        self.username = 'test_user'
        self.password = 'test_password'
        self.email = 'test_email@example.com'
        self.admin_user = User.objects.create_superuser(
            email=self.email,
            username=self.username,
            password=self.password)

        manager = TranslationManager()
        manager.load_data_from_po()

    def test_loaded_entry(self):
        """
        Tests that test locale was loaded correctly
        """
        entry = TranslationEntry.objects.get(original='test-case1')

        self.assertTrue(entry.is_published)
        self.assertEqual(entry.language, 'cs')
        self.assertEqual(entry.translation, 'test-case1_translation')
        self.assertEqual(entry.domain, 'django')
        self.assertEqual(entry.locale_path, 'tests/locale')
        self.assertEqual(entry.locale_parent_dir, 'tests')
