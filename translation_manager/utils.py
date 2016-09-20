
import os

from django.db.models import Q

from .settings import get_settings


def get_relative_locale_path(pofile):
    "Returns relative path of locale dir to project root dir ['/foo/bar', '/foo/bar/locale'] => 'locale'"
    locale_dir = os.path.dirname(os.path.dirname(os.path.dirname(pofile)))
    rel_path = os.path.relpath(locale_dir, get_settings('TRANSLATIONS_BASE_DIR'))
    return rel_path


def get_locale_parent_dirname(pofile):
    "Returns name of locale's dir parent ['/foo/bar', '/foo/bar/locale'] => 'bar'"
    locale_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(pofile))))
    dirname = os.path.relpath(locale_dir, os.path.join(locale_dir, ".."))
    return dirname


def get_dirname_from_lang(lang):
    "Converts lang in format en-gb to format en_GB"
    dirname = lang
    if len(lang) > 2:
        dirname = lang[:2] + "_" + lang[3:].upper()
    return dirname


def get_lang_from_dirname(dirname):
    "Converts lang in format en_GB to format en-gb"
    lang = dirname
    if len(dirname) > 2:
        lang = dirname[:2] + "-" + lang[3:].lower()
    return lang


def filter_queryset(qs, options):
    qs = qs.filter(is_published=True)
    if options:
        filter_ = options[0]
        q = Q(original__contains=filter_)
        for filter_ in options[1:]:
            q = q | Q(original__contains=filter_)
        qs = qs.filter(q)
    return qs
