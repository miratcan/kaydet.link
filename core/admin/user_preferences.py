from django.contrib import admin

from core.admin.base import BaseModelAdmin
from core.models import UserPreferences


@admin.register(UserPreferences)
class UserPreferencesAdmin(BaseModelAdmin):
    list_display = ('user', 'summary_mails')
    list_display_links = ('user',)
    search_fields = ('user__username', 'bio')
    ordering = ('user__username',)
    autocomplete_fields = ('user',)
    list_select_related = ('user',)
