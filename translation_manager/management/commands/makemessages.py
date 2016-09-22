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
        parser.add_argument('--locale', '-l', default=[], dest='locale', action='append',
                            help='Creates or updates the message files for the given locale(s) (e.g. pt_BR). '
                                 'Can be used multiple times.'),
        parser.add_argument('--exclude', '-x', default=[], dest='exclude', action='append',
                            help='Locales to exclude. Default is none. Can be used multiple times.'),
        parser.add_argument('--domain', '-d', default=get_settings('TRANSLATIONS_DOMAINS') or ['django', 'djangojs'],
                            dest='domain',
                            help='The domain of the message files (default: "django").'),
        parser.add_argument('--all', '-a', action='store_true', dest='all',
                            default=True, help='Updates the message files for all existing locales.'),
        parser.add_argument('--extension', '-e', dest='extensions',
                            help='The file extension(s) to examine (default: "html,txt", or "js" if the domain is "djangojs"). Separate multiple extensions with commas, or use -e multiple times.',
                            action='append'),
        parser.add_argument('--symlinks', '-s', action='store_true', dest='symlinks',
                            default=False,
                            help='Follows symlinks to directories when examining source code and templates for translation strings.'),
        parser.add_argument('--ignore', '-i', action='append', dest='ignore_patterns',
                            default=get_settings('TRANSLATIONS_IGNORED_PATHS') or [], metavar='PATTERN',
                            help='Ignore files or directories matching this glob-style pattern. Use multiple times to ignore more.'),
        parser.add_argument('--no-default-ignore', action='store_false', dest='use_default_ignore_patterns',
                            default=True,
                            help="Don't ignore the common glob-style patterns 'CVS', '.*', '*~' and '*.pyc'."),
        parser.add_argument('--no-wrap', action='store_true', dest='no_wrap',
                            default=False, help="Don't break long message lines into several lines."),
        parser.add_argument('--no-location', action='store_true', dest='no_location',
                            default=False, help="Don't write '#: filename:line' lines."),
        parser.add_argument('--no-obsolete', action='store_true', dest='no_obsolete',
                            default=False, help="Remove obsolete message strings."),
        parser.add_argument('--keep-pot', action='store_true', dest='keep_pot',
                            default=False, help="Keep .pot file after making messages. Useful when debugging."),

    def gettext_angular_js(self):
        all_files = self.find_files(get_settings('TRANSLATION_API_CLIENT_APP_SRC_PATH'))
        if all_files:
            temp_dir = os.path.join(get_settings('TRANSLATIONS_BASE_DIR'), 'angularjs_temp')
            os.mkdir(temp_dir)
            pattern = re.compile("{{\s*(\"|\')\s*[-_a-zA-Z0-9]+\s*(\"|\')\s*\|\s*translate\s*}}")
            for file in all_files:
                temp_file_path = os.path.join(temp_dir,
                                              file.path.replace(settings.TRANSLATION_API_CLIENT_APP_SRC_PATH, '')[1:])
                temp_dir_path = os.path.join(temp_dir,
                                             file.dirpath.replace(settings.TRANSLATION_API_CLIENT_APP_SRC_PATH, '')[1:])
                os.makedirs(temp_dir_path, exist_ok=True)
                output_file = open(temp_file_path, 'w+')
                html_file = open(file.path, 'r')
                text_in_file = html_file.read()
                html_file.close()
                iterator = pattern.finditer(text_in_file)
                for match in iterator:
                    translation_string = re.search('(\"|\')\s*[-_a-zA-Z0-9]+\s*(\"|\')', match.group())
                    gettext_string = '%s(%s);' % ('gettext', translation_string.group())
                    output_file.write(gettext_string)
                output_file.close()

    def handle(self, *args, **options):
        if get_settings('TRANSLATIONS_AUTO_CREATE_LANGUAGE_DIRS'):
            for language, language_name in settings.LANGUAGES:
                for locale in settings.LOCALE_PATHS:
                    language_dir_path = "%s/%s" % (str(locale), str(language))
                    if not os.path.isdir(language_dir_path):
                        os.mkdir(language_dir_path)

        self.manager = Manager()

        if get_settings('TRANSLATIONS_MAKE_BACKUPS'):
            self.manager.backup_po_to_db()

        self.angular_domain = False

        if 'django' in options['domain']:
            kwargs = deepcopy(options)
            kwargs.update({'domain': 'django'})
            super(Command, self).handle(*args, **kwargs)

        if get_settings('TRANSLATION_ENABLE_API_ANGULAR_JS'):
            self.domain = 'angularjs'
            self.extensions = ['.html']
            self.gettext_angular_js()
            self.angular_domain = True
            kwargs = deepcopy(options)
            kwargs.update({'domain': 'djangojs'})
            kwargs.update({'extensions': ['.html']})
            workdir = os.getcwd()
            temp_dir = os.path.join(get_settings('TRANSLATIONS_BASE_DIR'), 'angularjs_temp')
            os.chdir(temp_dir)
            super(Command, self).handle(*args, **kwargs)
            options['extensions'] = []
            self.angular_domain = False
            os.chdir(workdir)

            translation_temp_dir_path = os.path.join(get_settings('TRANSLATIONS_BASE_DIR'), 'angularjs_temp')
            if os.path.exists(translation_temp_dir_path):
                shutil.rmtree(os.path.join(translation_temp_dir_path))

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
                self.ignore_patterns = get_settings('TRANSLATION_API_IGNORED_PATHS')
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
            os.makedirs(basedir)
        if self.angular_domain:
            os.rename(os.path.join(basedir, '%s.po' % 'djangojs'), os.path.join(basedir, '%s.po' % 'angularjs'))
            pofile = os.path.join(basedir, '%s.po' % 'angularjs')
        else:
            pofile = os.path.join(basedir, '%s.po' % str(self.domain))
        # load data from po file to db
        if os.path.dirname(potfile) in settings.LOCALE_PATHS:
            self.manager.store_to_db(pofile, locale)
