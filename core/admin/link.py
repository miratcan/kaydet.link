from django.contrib import admin

from core.admin.base import BaseModelAdmin
from core.models import Link


@admin.register(Link)
class LinkAdmin(BaseModelAdmin):
    list_display = ('__str__', 'url', 'save_count', 'comment_count', 'created_at')
    list_display_links = ('__str__',)
    search_fields = ('url',)
    ordering = ('-last_saved_at', '-created_at')
