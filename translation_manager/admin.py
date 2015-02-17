from functools import update_wrapper

from django import VERSION
from django.contrib import admin
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from .manager import Manager
from .models import TranslationEntry, TranslationBackup
from .signals import post_save
from .widgets import add_styles
from .utils import filter_queryset
from .settings import get_settings


filter_excluded_fields = lambda fields: [field for field in fields if field not in get_settings('TRANSLATIONS_ADMIN_EXCLUDE_FIELDS')]


class TranslationEntryAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    save_on_top = True

    default_fields = ['original', 'language', 'get_hint', 'translation', 'occurrences', 'locale_parent_dir', 'domain']

    list_fields = filter_excluded_fields(get_settings('TRANSLATIONS_ADMIN_FIELDS'))
    if not list_fields:
        list_fields = filter_excluded_fields(default_fields)

    fields = default_fields
    list_display = list_fields
    list_editable = ('translation',)
    ordering = ('original', 'language')
    readonly_fields = list(default_fields)
    readonly_fields.remove('original')
    search_fields = filter_excluded_fields(['original', 'translation', 'occurrences'])
    list_per_page = 100

    if (VERSION[0] == 1 and VERSION[1] >= 4) or VERSION[0] > 1:
        from .filters import TranslationStateFilter, CustomFilter
        list_filter = ['language', 'locale_parent_dir', 'domain', TranslationStateFilter]
        if get_settings('TRANSLATIONS_CUSTOM_FILTERS'):
            list_filter.append(CustomFilter)
    else:
        list_filter = ('language', 'locale_parent_dir', 'domain')

    if (VERSION[0] == 1 and VERSION[1] >= 7) or VERSION[0] > 1:
        change_list_template = "admin/translation_manager/change_list.7.html"
    else:
        change_list_template = "admin/translation_manager/change_list.2.html"

    list_filter = filter_excluded_fields(list_filter)

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(TranslationEntryAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'translation':
            add_styles(formfield.widget, u'height: 26px;')
        return formfield

    def get_urls(self):
        try:
            from django.conf.urls import patterns, url
        except ImportError:
            # Old django fix
            from django.conf.urls.defaults import patterns, url
 
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)
 
        try:
            info = self.model._meta.app_label, self.model._meta.model_name
        except AttributeError:
            # Old django fix
            info = self.model._meta.app_label, self.model._meta.module_name
 
        urls = patterns('',
            url(r'^make/$', wrap(self.make_translations_view), name='%s_%s_make' % info),
            url(r'^compile/$', wrap(self.compile_translations_view), name='%s_%s_compile' % info),
            url(r'^load_from_po/$', wrap(self.load_from_po_view), name='%s_%s_load' % info),
        )
 
        super_urls = super(TranslationEntryAdmin, self).get_urls()
 
        return urls + super_urls

    def get_queryset(self, request):
        qs = super(TranslationEntryAdmin, self).get_queryset(request=request)
        return filter_queryset(qs)

    # older django
    def queryset(self, request):
        qs = super(TranslationEntryAdmin, self).queryset(request=request)
        return filter_queryset(qs)


    def load_from_po_view(self, request):
        if request.user.has_perm('translation_manager.load'):
            manager = Manager()
            manager.load_data_from_po()

            self.message_user(request, _("admin-translation_manager-data-loaded_from_po"))
        return HttpResponseRedirect(reverse("admin:translation_manager_translationentry_changelist"))

    def make_translations_view(self, request):
        call_command('makemessages')

        self.message_user(request, _("admin-translation_manager-translations_made"))
        return HttpResponseRedirect(reverse("admin:translation_manager_translationentry_changelist"))

    def compile_translations_view(self, request):
        manager = Manager()
        for language, language_name in settings.LANGUAGES:
            manager.update_po_from_db(lang=language)
        post_save.send(sender=None, request=request)

        self.message_user(request, _("admin-translation_manager-translations_compiled"))
        return HttpResponseRedirect(reverse("admin:translation_manager_translationentry_changelist"))

    def get_changelist(self, request, **kwargs):

        from .views import TranslationChangeList
        return TranslationChangeList


def restore(modeladmin, request, queryset):
    for backup in queryset:
        backup.restore()
restore.short_description = _("admin-translation_manager-backups_restore_option")


class TranslationBackupAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    actions = [restore]
    save_on_top = True
    fields = ('created', 'language', 'locale_parent_dir', 'domain', 'content')
    list_display = ('created', 'language', 'locale_parent_dir', 'domain')
    list_filter = ('created', 'language', 'locale_parent_dir', 'domain')
    readonly_fields = ('created', 'language', 'locale_parent_dir', 'domain')


admin.site.register(TranslationEntry, TranslationEntryAdmin)
admin.site.register(TranslationBackup, TranslationBackupAdmin)
