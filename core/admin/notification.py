from django.contrib import admin

from core.admin.base import BaseModelAdmin
from core.models import Notification


@admin.register(Notification)
class NotificationAdmin(BaseModelAdmin):
    list_display = ('actor', 'type', 'recipient', 'seen', 'created_at')
    list_display_links = ('actor',)
    search_fields = ('actor__username', 'recipient__username')
    ordering = ('-created_at',)
    autocomplete_fields = ('actor', 'recipient', 'target_link', 'target_comment')
    list_select_related = ('actor', 'recipient')
