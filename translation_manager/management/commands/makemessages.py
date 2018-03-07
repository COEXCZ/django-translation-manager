# -*- coding: utf-8 -*-
from copy import deepcopy

import os
import re
import shutil

from django.core.management.commands.makemessages import Command as OriginCommand
from django.conf import settings

from translation_manager.manager import Manager
from translation_manager.settings import get_settings


class Command(OriginCommand):

    def add_arguments(self, parser):

        # Call method of supperclass to give all parser arguments
        parser = super(Command, self).add_arguments(parser)
        # here is place to add new arguments.

        return parser

    def gettext_angular_js(self):
        all_files = self.find_files(get_settings('TRANSLATIONS_API_CLIENT_APP_SRC_PATH'))
        if all_files:
            temp_dir = os.path.join(get_settings('TRANSLATIONS_BASE_DIR'), 'angularjs_temp')
            os.makedirs(temp_dir, exist_ok=True)
            regexes = get_settings('TRANSLATIONS_API_TRANSLATION_STRINGS_REGEX_LIST')
            regex_legacy = get_settings('TRANSLATIONS_API_TRANSLATION_STRINGS_REGEX')
            if regex_legacy:
                regexes.append(regex_legacy)
            for file in all_files:
                temp_file_path = os.path.join(temp_dir,
                                              file.path.replace(settings.TRANSLATIONS_API_CLIENT_APP_SRC_PATH, '')[1:])
                temp_dir_path = os.path.join(temp_dir, file.dirpath.replace(
                    settings.TRANSLATIONS_API_CLIENT_APP_SRC_PATH, '')[1:])
                os.makedirs(temp_dir_path, exist_ok=True)
                output_file = open(temp_file_path, 'w+')
                html_file = open(file.path, 'r')
                text_in_file = html_file.read()
                html_file.close()
                for regex in regexes:
                    pattern = re.compile(regex)
                    translation_strings = pattern.findall(text_in_file)
                    for translation_string in translation_strings:
                        gettext_string = '%s(\'%s\');' % ('gettext', translation_string)
                        output_file.write(gettext_string)
                output_file.close()
            return True
        else:
            return False

    def handle(self, *args, **options):
        if get_settings('TRANSLATIONS_AUTO_CREATE_LANGUAGE_DIRS'):
            for language, language_name in settings.LANGUAGES:
                for locale in settings.LOCALE_PATHS:
                    language_dir_path = os.path.join(locale, language)
                    if not os.path.isdir(language_dir_path):
                        os.mkdir(language_dir_path)

        self.manager = Manager()

        if get_settings('TRANSLATIONS_MAKE_BACKUPS'):
            self.manager.backup_po_to_db()

        self.angular_domain = False

        os.chdir(get_settings('TRANSLATIONS_PROJECT_BASE_DIR'))

        if 'django' in options['domain']:
            kwargs = deepcopy(options)
            kwargs.update({'domain': 'django'})
            super(Command, self).handle(*args, **kwargs)

        if get_settings('TRANSLATIONS_ENABLE_API_ANGULAR_JS'):
            self.domain = 'angularjs'
            self.extensions = ['.html', '.js']
            created = self.gettext_angular_js()

            if created:
                self.angular_domain = True
                kwargs = deepcopy(options)
                kwargs.update({'domain': 'djangojs'})
                kwargs.update({'extensions': ['html', 'js']})
                temp_dir = os.path.join(get_settings('TRANSLATIONS_BASE_DIR'), 'angularjs_temp')
                os.chdir(temp_dir)
                super(Command, self).handle(*args, **kwargs)
                options['extensions'] = []
                self.angular_domain = False

            translation_temp_dir_path = os.path.join(get_settings('TRANSLATIONS_BASE_DIR'), 'angularjs_temp')
            if os.path.exists(translation_temp_dir_path):
                shutil.rmtree(translation_temp_dir_path)

            os.chdir(get_settings('TRANSLATIONS_PROJECT_BASE_DIR'))

        if 'djangojs' in options['domain']:
            kwargs = deepcopy(options)
            kwargs.update({'domain': 'djangojs'})
            super(Command, self).handle(*args, **kwargs)

        try:
            from django.core.management.commands.makemessages import make_messages as old_make_messages
        except ImportError:
            self.manager.postprocess()

    def find_files(self, root):
        if self.domain == 'angularjs':
            if root:
                old_ignore_patterns = self.ignore_patterns
                self.ignore_patterns = get_settings('TRANSLATIONS_API_IGNORED_PATHS')
                all_files = super(Command, self).find_files(root)
                self.ignore_patterns = old_ignore_patterns
                return all_files
            else:
                return []
        return super(Command, self).find_files(root)

    def write_po_file(self, potfile, locale):
        super(Command, self).write_po_file(potfile, locale)

        basedir = os.path.join(os.path.dirname(potfile), locale, 'LC_MESSAGES')
        if not os.path.isdir(basedir):
            os.makedirs(basedir, exist_ok=True)
        if self.angular_domain:
            os.rename(os.path.join(basedir, '%s.po' % 'djangojs'), os.path.join(basedir, '%s.po' % 'angularjs'))
            pofile = os.path.join(basedir, '%s.po' % 'angularjs')
        else:
            pofile = os.path.join(basedir, '%s.po' % str(self.domain))
        # load data from po file to db
        if os.path.dirname(potfile).rstrip('/') in [path.rstrip('/') for path in settings.LOCALE_PATHS]:
            self.manager.store_to_db(pofile, locale)
