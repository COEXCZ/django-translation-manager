from django import VERSION
from django.contrib import admin
from django.utils.text import capfirst as cf
from django.utils.translation import ugettext as _

from . import choices
from .settings import get_settings

if (VERSION[0] == 1 and VERSION[1] >= 4) or VERSION[0] > 1:
    class TranslationStateFilter(admin.SimpleListFilter):
        title = _('admin-translation_manager-translation_state_filter-title')
        parameter_name = 'state'

        def lookups(self, request, model_admin):
            return (
                (choices.TRANSLATIONS_TRANSLATED, _('admin-translation_manager-translation_state_filter-translated')),
                (choices.TRANSLATIONS_UNTRANSLATED, _('admin-translation_manager-translation_state_filter-untranslated')),
            )

        def queryset(self, request, queryset):
            all_count = queryset.count()
            translated_count = queryset.exclude(translation='').count()
            untranslated_count = all_count - translated_count

            translated_title = u'{translated_label} ({translated_count} / {all_count})'.format(
                translated_label=self.lookup_choices[0][1],
                translated_count=translated_count,
                all_count=all_count,
            )

            untranslated_title = u'{translated_label} ({untranslated_count} / {all_count})'.format(
                translated_label=self.lookup_choices[1][1],
                untranslated_count=untranslated_count,
                all_count=all_count,
            )

            self.lookup_choices = [
                (choices.TRANSLATIONS_TRANSLATED, cf(translated_title)),
                (choices.TRANSLATIONS_UNTRANSLATED, cf(untranslated_title)),
            ]

            if self.value() == choices.TRANSLATIONS_TRANSLATED:
                return queryset.exclude(translation="")
            if self.value() == choices.TRANSLATIONS_UNTRANSLATED:
                return queryset.filter(translation="")

    class CustomFilter(admin.SimpleListFilter):
        title = _('admin-translation_manager-translation_custom_filter-title')
        parameter_name = 'custom_filter'

        def __init__(self, *args, **kwargs):
            self.title = cf(_(get_settings('TRANSLATIONS_CUSTOM_FILTERS_LABEL')))
            super(CustomFilter, self).__init__(*args, **kwargs)

        def lookups(self, request, model_admin):
            return [(i, cf(_(label))) for i, (group_filter, label) in enumerate(get_settings('TRANSLATIONS_CUSTOM_FILTERS'))]

        def queryset(self, request, queryset):
            active_filter = self.value()
            print(active_filter)
            if not active_filter:
                return queryset
            else:
                filter_value, label = get_settings('TRANSLATIONS_CUSTOM_FILTERS')[int(active_filter)]
                return queryset.filter(original__regex=filter_value)
