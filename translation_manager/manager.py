# -*- coding: utf-8 -*-

import codecs
import os
import polib

from datetime import datetime

from django import VERSION
from django.conf import settings

from glob import glob

from .choices import TRANSLATIONS_MODE_PROMISCUOUS
from .models import TranslationEntry, TranslationBackup
from .utils import get_relative_locale_path, get_locale_parent_dirname, get_dirname_from_lang, get_lang_from_dirname
from .settings import get_settings


class Manager(object):

    def __init__(self, *args, **kwargs):
        super(Manager, self).__init__(*args, **kwargs)

        self.tors = {}

    def store_to_db(self, pofile, locale, store_translations=False):
        language = get_lang_from_dirname(locale)
        domain = os.path.splitext(os.path.basename(pofile))[0]
        messages = polib.pofile(pofile)
        translations = TranslationEntry.objects.filter(language=language)

        tdict = {}
        for t in translations:
            if t.original not in tdict:
                tdict.update({t.original: {}})
            tdict[t.original][t.language] = t.translation

        for m in messages:
            occs = []
            for occ in m.occurrences:
                path = ":".join(occ)
                occs.append(path)

            if store_translations:
                translation = m.msgstr
            else:
                translation = ""

            locale_path = get_relative_locale_path(pofile)

            if os.path.split(pofile)[-1] == 'angularjs.po':
                locale_dir_name = ''
            else:
                locale_dir_name = get_locale_parent_dirname(pofile)
            t, created = TranslationEntry.objects.get_or_create(
                original=m.msgid,
                language=language,
                locale_path=locale_path,
                domain=domain,
                defaults={
                    "occurrences": "\n".join(occs),
                    "translation": translation,
                    "locale_parent_dir": locale_dir_name,
                    "is_published": True,
                }
            )

            if locale_path not in self.tors:
                self.tors[locale_path] = {}
            if language not in self.tors[locale_path]:
                self.tors[locale_path][language] = {}
            if domain not in self.tors[locale_path][language]:
                self.tors[locale_path][language][domain] = []
            self.tors[locale_path][language][domain].append(t.original)

    ############################################################################

    def backup_po_to_db(self):
        """ Backup Po file to db model """


        for lang, lang_name in settings.LANGUAGES:
            for path in settings.LOCALE_PATHS:
                po_pattern = os.path.join(path, get_dirname_from_lang(lang), "LC_MESSAGES", "*.po")
                for pofile in glob(po_pattern):
                    if settings.DEBUG:
                        print ("Backuping", pofile)

                    domain = os.path.splitext(os.path.basename(pofile))[0]
                    with codecs.open(pofile, 'r', 'utf-8') as pofile_opened:
                        content = pofile_opened.read()
                        backup = TranslationBackup(
                            language=lang,
                            locale_path=get_relative_locale_path(pofile),
                            domain=domain,
                            locale_parent_dir=get_locale_parent_dirname(pofile),
                            content=content,
                        )
                        backup.save()

                    if get_settings('TRANSLATIONS_CLEAN_PO_AFTER_BACKUP'):
                        with open(pofile, 'w') as pofile_opened:
                            pofile_opened.write('')


    ############################################################################


    def update_po_from_db(self, lang):

        translations = TranslationEntry.objects.filter(
            language=lang,
            is_published=True
        ).exclude(
            translation=""
        ).order_by("original")

        locale_params = TranslationEntry.objects.filter(is_published=True).order_by('locale_path', 'domain')

        forced_locale_paths = get_settings('TRANSLATIONS_UPDATE_FORCED_LOCALE_PATHS')
        if forced_locale_paths:
            translations = translations.filter(locale_path__in=forced_locale_paths)
            locale_params = locale_params.filter(locale_path__in=forced_locale_paths)

        locale_params = locale_params.values_list('locale_path', 'domain')
        locale_params = list(set(locale_params))

        for locale_path, domain in locale_params:
            lang_dir_path = os.path.abspath(
                os.path.join(get_settings('TRANSLATIONS_BASE_DIR'), locale_path, get_dirname_from_lang(lang)))
            if not os.path.isdir(lang_dir_path):
                os.mkdir(lang_dir_path)
                os.mkdir(os.path.join(lang_dir_path, 'LC_MESSAGES'))

            pofile_path = os.path.join(get_settings('TRANSLATIONS_BASE_DIR'), locale_path, get_dirname_from_lang(lang),
                                       'LC_MESSAGES',
                                               "%s.po" % domain)
            mofile_path = os.path.join(get_settings('TRANSLATIONS_BASE_DIR'), locale_path, get_dirname_from_lang(lang),
                                       'LC_MESSAGES',
                                               "%s.mo" % domain)

            if not os.path.exists(pofile_path):
                if settings.DEBUG:
                    print ("Po file '%s' does't exists, it will be created" % pofile_path)

            now = datetime.now()
            pofile = polib.POFile()
            pofile.metadata = {
                'Project-Id-Version': '0.1',
                'Report-Msgid-Bugs-To': '%s' % settings.DEFAULT_FROM_EMAIL,
                'POT-Creation-Date': now.strftime("%Y-%m-%d %H:%M:%S"),
                'PO-Revision-Date': now.strftime("%Y-%m-%d %H:%M:%S"),
                'Last-Translator': 'Server <%s>' % settings.SERVER_EMAIL,
                'Language-Team': 'English <%s>' % settings.DEFAULT_FROM_EMAIL,
                'MIME-Version': '1.0',
                'Content-Type': 'text/plain; charset=utf-8',
                'Content-Transfer-Encoding': '8bit',
            }

            for translation in translations.filter(locale_path=locale_path, domain=domain):
                entry = polib.POEntry(
                    msgid=translation.original,
                    msgstr=translation.translation,
                    occurrences=[occ.split(":") for occ in translation.occurrences.split()]
                )
                pofile.append(entry)

            pofile.save(pofile_path)
            pofile.save_as_mofile(mofile_path)

    ############################################################################

    def postprocess(self):
        TranslationEntry.objects.all().update(is_published=False)
        for locale_path, languages in self.tors.items():
            TranslationEntry.objects.filter(locale_path=locale_path).update(is_published=False)
            for language, domains in languages.items():
                for domain, tors in domains.items():
                    tors = list(set(tors))
                    TranslationEntry.objects.filter(
                        locale_path=locale_path,
                        language=language,
                        domain=domain,
                        original__in=tors
                    ).update(is_published=True)

        if get_settings('TRANSLATIONS_MODE') == TRANSLATIONS_MODE_PROMISCUOUS:
            published = TranslationEntry.objects.filter(is_published=True).order_by("original", 'language', 'locale_path')
            for trans in published:
                if VERSION[:2] in [(1, 2), (1, 3)]:
                    locale_paths = [os.path.relpath(path, get_settings('TRANSLATIONS_BASE_DIR')) for path in settings.LOCALE_PATHS]
                else:
                    locale_paths = self.tors.keys()

                for locale_path in locale_paths:
                    locale_parent_dir = get_locale_parent_dirname(
                        os.path.join(
                            get_settings('TRANSLATIONS_BASE_DIR'),
                            locale_path,
                            get_dirname_from_lang(trans.language),
                            'LC_MESSAGES',
                            "django.po"
                        )
                    )

                    t, created = TranslationEntry.objects.get_or_create(
                        original=trans.original,
                        language=trans.language,
                        locale_path=locale_path,
                        domain=trans.domain,
                        defaults={
                            "occurrences": trans.occurrences,
                            "translation": trans.translation,
                            "locale_parent_dir": locale_parent_dir,
                            "is_published": True,
                        }
                    )
            TranslationEntry.objects.filter(original__in=published.values_list('original', flat=True)).update(is_published=True)

    ############################################################################

    def load_data_from_po(self):
        import os

        for lang, lang_name in settings.LANGUAGES:
            for path in settings.LOCALE_PATHS:
                locale = get_dirname_from_lang(lang)
                po_pattern = os.path.join(path, locale, "LC_MESSAGES", "*.po")
                for pofile in glob(po_pattern):
                    if settings.DEBUG:
                        print ("processing pofile", pofile)
                    self.store_to_db(pofile=pofile, locale=locale, store_translations=True)

        self.postprocess()
