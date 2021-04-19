import django
from django.core.management import call_command
from django.contrib.auth.models import User
from django.test import TestCase, override_settings

from translation_manager import tasks
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

    def test_makemessages_django(self):
        if django.get_version() >= "3.1":
            call_command('makemessages', '--all')
        else:
            call_command('makemessages')

    @override_settings(TRANSLATIONS_PROCESSING_METHOD='async_django_rq')
    def test_makemessages_django_rq_single_run(self):
        from django_rq import get_queue, get_worker

        queue = get_queue('default')
        queue.enqueue(tasks.makemessages_task)

        get_worker().work(burst=True)

    @override_settings(TRANSLATIONS_PROCESSING_METHOD='async_django_rq')
    def test_makemessages_django_tq_more_jobs(self):
        from django_rq import get_queue, get_worker

        queue = get_queue('default')
        queue.enqueue(tasks.makemessages_task)
        queue.enqueue(tasks.makemessages_task)
        queue.enqueue(tasks.makemessages_task)

        get_worker().work(burst=True)
