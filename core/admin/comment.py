from django.contrib import admin

from core.admin.base import BaseModelAdmin
from core.models import Comment


@admin.register(Comment)
class CommentAdmin(BaseModelAdmin):
    list_display = ('posted_by', 'link', 'created_at')
    list_display_links = ('posted_by',)
    search_fields = ('body',)
    ordering = ('-created_at',)
    autocomplete_fields = ('posted_by', 'link')
    list_select_related = ('posted_by', 'link')
