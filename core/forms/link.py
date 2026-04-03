from django import forms
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from core.models import Bookmark, Tag
from core.services.bookmark import BookmarkService


class BookmarkForm(forms.Form):
    url = forms.URLField(
        max_length=2000,
        widget=forms.URLInput(attrs={'placeholder': 'https://...'}),
    )
    note = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': _('Why are you saving this?')}),
    )
    tag_names = forms.CharField(
        required=False,
        label=_('Tags'),
        help_text=_('Comma-separated tags'),
        widget=forms.TextInput(attrs={'placeholder': _('python, django, web')}),
    )

    def save(self, user, parent=None):
        tags = self._parse_tags()
        bookmark = BookmarkService.create_bookmark(
            user=user,
            url=self.cleaned_data.get('url'),
            note=self.cleaned_data.get('note', ''),
            tags=tags,
            parent=parent,
        )
        return bookmark

    def _parse_tags(self):
        raw = self.cleaned_data.get('tag_names', '')
        if not raw:
            return []
        tag_names = [t.strip().lower() for t in raw.split(',') if t.strip()]
        tags = []
        for name in tag_names:
            slug = slugify(name, allow_unicode=True)
            if not slug:
                continue
            tag, _created = Tag.objects.get_or_create(
                slug=slug,
                defaults={'name': name},
            )
            tags.append(tag)
        return tags


class BookmarkEditForm(forms.ModelForm):
    tag_names = forms.CharField(
        required=False,
        label=_('Tags'),
        help_text=_('Comma-separated tags'),
        widget=forms.TextInput(attrs={'placeholder': _('python, django, web')}),
    )

    class Meta:
        model = Bookmark
        fields = ('note',)
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial['tag_names'] = ', '.join(
                self.instance.tags.values_list('name', flat=True),
            )

    def save(self, commit=True):
        bookmark = super().save(commit=commit)
        if commit:
            self._save_tags(bookmark)
        return bookmark

    def _save_tags(self, bookmark):
        raw = self.cleaned_data.get('tag_names', '')
        if not raw:
            bookmark.tags.clear()
            return
        tag_names = [t.strip().lower() for t in raw.split(',') if t.strip()]
        tags = []
        for name in tag_names:
            slug = slugify(name, allow_unicode=True)
            if not slug:
                continue
            tag, _created = Tag.objects.get_or_create(
                slug=slug,
                defaults={'name': name},
            )
            tags.append(tag)
        bookmark.tags.set(tags)
