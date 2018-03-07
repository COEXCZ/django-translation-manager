from email.policy import HTTP

import requests

from functools import update_wrapper

import rest_framework
from django.contrib import admin

try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse

from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse
from django.http.response import HttpResponseBadRequest
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from rest_framework.status import is_success

from .manager import Manager
from .models import TranslationEntry, TranslationBackup, RemoteTranslationEntry, ProxyTranslationEntry
from .signals import post_save
from .widgets import add_styles
from .utils import filter_queryset
from .settings import get_settings

from translation_manager import tasks

from django.core.cache import cache

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

    from .filters import TranslationStateFilter, CustomFilter
    list_filter = ['language', 'locale_parent_dir', 'domain', TranslationStateFilter]
    if get_settings('TRANSLATIONS_CUSTOM_FILTERS'):
        list_filter.append(CustomFilter)
    else:
        list_filter = ('language', 'locale_parent_dir', 'domain')

    change_list_template = "admin/translation_manager/change_list.html"

    list_filter = filter_excluded_fields(list_filter)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['make_translations_running'] = cache.get('make_translations_running')
        extra_context['remote_url'] = settings.TRANSLATIONS_SYNC_REMOTE_URL
        return super(TranslationEntryAdmin, self).changelist_view(request, extra_context=extra_context)

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(TranslationEntryAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'translation':
            add_styles(formfield.widget, u'height: 26px;')
        return formfield

    def get_urls(self):
        from django.conf.urls import url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        urls = [
            url(r'^make/$', wrap(self.make_translations_view), name='%s_%s_make' % info),
            url(r'^compile/$', wrap(self.compile_translations_view), name='%s_%s_compile' % info),
            url(r'^load_from_po/$', wrap(self.load_from_po_view), name='%s_%s_load' % info),
            url(r'^get_make_translations_status/$', wrap(self.get_make_translations_status),
                name='%s_%s_status' % info),
            url(r'^sync/$', wrap(self.sync_translations), name='%s_%s_sync' % info),
        ]

        super_urls = super(TranslationEntryAdmin, self).get_urls()

        return urls + super_urls

    def get_queryset(self, request):
        qs = super(TranslationEntryAdmin, self).get_queryset(request=request)
        return filter_queryset(qs, get_settings('TRANSLATIONS_QUERYSET_FORCE_FILTERS'))

    # older django
    def queryset(self, request):
        qs = super(TranslationEntryAdmin, self).queryset(request=request)
        return filter_queryset(qs, get_settings('TRANSLATIONS_QUERYSET_FORCE_FILTERS'))

    def get_make_translations_status(self, request):
        if cache.get('make_translations_running'):
            result = {"running": True}
        else:
            result = {"running": False}

        return JsonResponse(result)

    def load_from_po_view(self, request):
        if request.user.has_perm('translation_manager.load'):
            manager = Manager()
            manager.load_data_from_po()

            self.message_user(request, _("admin-translation_manager-data-loaded_from_po"))
        return HttpResponseRedirect(reverse("admin:translation_manager_translationentry_changelist"))

    def make_translations_view(self, request):
        translation_mode = str(get_settings('TRANSLATIONS_PROCESSING_METHOD'))
        if not cache.get('make_translations_running'):
            cache.set('make_translations_running', True)
            try:
                if translation_mode == 'sync':
                    tasks.makemessages_task()
                elif translation_mode == 'async_django_rq':
                    tasks.makemessages_task.delay()
            except Exception:
                if cache.get(('make_translations_running')):
                    cache.set('make_translations_running', False)

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

    def sync_translations(self, request):
        if not request.user.has_perm('translation_manager.sync'):
            return HttpResponseRedirect(reverse("admin:translation_manager_translationentry_changelist"))

        url = '{}?token={}'.format(
            get_settings('TRANSLATIONS_SYNC_REMOTE_URL'),
            get_settings('TRANSLATIONS_SYNC_REMOTE_TOKEN'),
        )

        remote_user = get_settings('TRANSLATIONS_SYNC_REMOTE_USER')
        remote_password = get_settings('TRANSLATIONS_SYNC_REMOTE_PASSWORD')

        if remote_user is not None and remote_password is not None:
            response = requests.get(url, verify=get_settings('TRANSLATIONS_SYNC_VERIFY_SSL'), auth=(remote_user, remote_password))
        else:
            response = requests.get(url, verify=get_settings('TRANSLATIONS_SYNC_VERIFY_SSL'))

        if not is_success(response.status_code):
            return HttpResponseBadRequest('Wrong response from remote TRM URL')

        data = response.json()

        RemoteTranslationEntry.objects.all().delete()

        for language, domains in data.items():
            for domain, translation_entries in domains.items():
                for original, translation_entry in translation_entries.items():
                    try:
                        main_entry = TranslationEntry.objects.get(language=language, original=original, domain=domain)
                    except TranslationEntry.DoesNotExist as e:
                        print('Missing: ', language, original, domain)
                        continue

                    RemoteTranslationEntry.objects.create(
                        translation=translation_entry['translation'],
                        changed=translation_entry['changed'],
                        translation_entry=main_entry
                    )

        return HttpResponseRedirect(reverse('admin:translation_manager_proxytranslationentry_changelist'))


class ProxyTranslationEntryAdmin(TranslationEntryAdmin):

    fields = ['original', 'language', 'get_hint', 'changed', 'translation', 'use_remote','remote_translation', 'remote_changed', 'domain']
    list_display = fields

    change_list_template = "admin/translation_manager/remote_change_list.html"

    def remote_translation(self, obj):
        """
        :param obj:
        :type obj: TranslationEntry
        :return:
        """
        return obj.remote_translation_entry.translation

    def remote_changed(self, obj):
        """
        :param obj:
        :type obj: TranslationEntry
        :return:
        """
        return obj.remote_translation_entry.changed

    def get_queryset(self, request):
        qs = super(ProxyTranslationEntryAdmin, self).get_queryset(request=request)
        return qs.exclude(remote_translation_entry=None).exclude(translation=F('remote_translation_entry__translation'))

    def use_remote(self, obj):
        """
        :param obj:
        :type obj: TranslationEntry
        :return:
        """

        if obj.remote_translation_entry:
            return mark_safe('<input type="button" data-id="{id}" class="btn btn-info btn-use-remote" value="{name}"/><xmp id="{id}" style="display: none">{remote_translation_value}</xmp>'.format(
                name=_("admin-translation_manager-use_remote-value"),
                remote_translation_value=obj.remote_translation_entry.translation,
                id=obj.pk
            ))

        return '-'


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
admin.site.register(ProxyTranslationEntry, ProxyTranslationEntryAdmin)
