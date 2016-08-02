# -*- coding: utf-8 -*-
from copy import deepcopy

import os
from optparse import make_option

from django.core.management.commands.makemessages import Command as OriginCommand
from django.core.management.base import NoArgsCommand
from django.conf import settings

from translation_manager.manager import Manager
from translation_manager.settings import get_settings


################################################################################

class Command(OriginCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--locale', '-l', default=None, dest='locale', action='append',
            help='Creates or updates the message files for the given locale(s) (e.g. pt_BR). '
                 'Can be used multiple times.'),
        make_option('--domain', '-d', default=get_settings('TRANSLATIONS_DOMAINS') or ['django', 'djangojs'], dest='domain',
            help='The domain of the message files (default: "django").'),
        make_option('--all', '-a', action='store_true', dest='all',
            default=True, help='Updates the message files for all existing locales.'),
        make_option('--extension', '-e', dest='extensions',
            help='The file extension(s) to examine (default: "html,txt", or "js" if the domain is "djangojs"). Separate multiple extensions with commas, or use -e multiple times.',
            action='append'),
        make_option('--symlinks', '-s', action='store_true', dest='symlinks',
            default=False, help='Follows symlinks to directories when examining source code and templates for translation strings.'),
        make_option('--ignore', '-i', action='append', dest='ignore_patterns',
            default=get_settings('TRANSLATIONS_IGNORED_PATHS') or [], metavar='PATTERN', help='Ignore files or directories matching this glob-style pattern. Use multiple times to ignore more.'),
        make_option('--no-default-ignore', action='store_false', dest='use_default_ignore_patterns',
            default=True, help="Don't ignore the common glob-style patterns 'CVS', '.*', '*~' and '*.pyc'."),
        make_option('--no-wrap', action='store_true', dest='no_wrap',
            default=False, help="Don't break long message lines into several lines."),
        make_option('--no-location', action='store_true', dest='no_location',
            default=False, help="Don't write '#: filename:line' lines."),
        make_option('--no-obsolete', action='store_true', dest='no_obsolete',
            default=False, help="Remove obsolete message strings."),
        make_option('--keep-pot', action='store_true', dest='keep_pot',
            default=False, help="Keep .pot file after making messages. Useful when debugging."),
    )

    # Django 1.4+ ****************************************************************

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

        for domain in options['domain']:
            kwargs = deepcopy(options)
            kwargs.update({'domain': domain})
            super(Command, self).handle(*args, **kwargs)

        try:
            from django.core.management.commands.makemessages import make_messages as old_make_messages
        except ImportError:
            self.manager.postprocess()

    def write_po_file(self, potfile, locale):
        super(Command, self).write_po_file(potfile, locale)

        basedir = os.path.join(os.path.dirname(potfile), locale, 'LC_MESSAGES')
        if not os.path.isdir(basedir):
            os.makedirs(basedir)
        pofile = os.path.join(basedir, '%s.po' % str(self.domain))

        # load data from po file to db
        if os.path.dirname(potfile) in settings.LOCALE_PATHS:
            self.manager.store_to_db(pofile, locale)
