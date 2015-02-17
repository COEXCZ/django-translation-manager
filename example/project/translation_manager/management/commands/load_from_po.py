# -*- coding: utf-8 -*-

from translation_manager.manager import Manager
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    can_import_settings = True


    def handle(self, *args, **options):
        manager = Manager()
        manager.load_data_from_po()