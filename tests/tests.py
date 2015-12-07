from django.test import TestCase
from django.contrib.auth.models import AnonymousUser, User


class TranslationCase(TestCase):
    def setUp(self):
        self.username = 'test_user'
        self.password = 'test_password'
        self.email = 'test_email@example.com'
        self.admin_user = User.objects.create_superuser(
            email=self.email,
            username=self.username,
            password=self.password)

    