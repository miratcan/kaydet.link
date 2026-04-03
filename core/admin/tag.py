from django.contrib import admin

from core.admin.base import BaseModelAdmin
from core.models import Tag


@admin.register(Tag)
class TagAdmin(BaseModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    list_display_links = ('name',)
    search_fields = ('name', 'slug')
    ordering = ('name',)
    prepopulated_fields = {'slug': ('name',)}
