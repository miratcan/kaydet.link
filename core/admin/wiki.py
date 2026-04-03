from django.contrib import admin

from core.admin.base import BaseModelAdmin
from core.models import Page


@admin.register(Page)
class PageAdmin(BaseModelAdmin):
    list_display = ('name', 'is_listed', 'updated_at')
    list_display_links = ('name',)
    search_fields = ('name', 'content')
    ordering = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('contributors',)
