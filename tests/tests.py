from django.test import TestCase
from django.contrib.auth.models import User

from translation_manager.manager import Manager as TranslationManager
from translation_manager.models import TranslationEntry
from django.core.management import call_command

from translation_manager import tasks

from translation_manager.settings import get_settings

if get_settings('TRANSLATIONS_PROCESSING_METHOD') == 'async_django_rq':
    from django_rq import get_queue, get_worker

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

    def test_makemessages_django_1_4_19(self):
        call_command('makemessages')

    if get_settings('TRANSLATIONS_PROCESSING_METHOD') == 'async_django_rq':
        def test_makemessages_django_rq_single_run(self):
            queue = get_queue('default')
            queue.enqueue(tasks.makemessages_task)

            get_worker().work(burst=True)

        def test_makemessages_django_tq_more_jobs(self):
            queue = get_queue('default')
            queue.enqueue(tasks.makemessages_task)
            queue.enqueue(tasks.makemessages_task)
            queue.enqueue(tasks.makemessages_task)

            get_worker().work(burst=True)
