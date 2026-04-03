from django import forms
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from core.models import Bookmark, Collection, Tag
from core.services.bookmark import BookmarkService


class BookmarkForm(forms.Form):
    url = forms.URLField(
        max_length=2000,
        widget=forms.URLInput(attrs={'placeholder': 'https://...'}),
    )
    note = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': _('Leave a note for your future self... What did you learn? Why is this useful?'),
        }),
    )
    tag_names = forms.CharField(
        required=False,
        label=_('Tags'),
        help_text=_('Comma-separated tags'),
        widget=forms.TextInput(attrs={'placeholder': _('python, django, web')}),
    )
    collections = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Collection.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        label=_('Collections'),
    )
    is_private = forms.BooleanField(
        required=False,
        initial=True,
        label=_('Private'),
        help_text=_('Only you can see this bookmark'),
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['collections'].queryset = (
                Collection.objects.filter(user=user).order_by('position', 'name')
            )

    def save(self, user, parent=None):
        tags = self._parse_tags()
        bookmark = BookmarkService.create_bookmark(
            user=user,
            url=self.cleaned_data.get('url'),
            note=self.cleaned_data.get('note', ''),
            tags=tags,
            parent=parent,
            is_private=self.cleaned_data.get('is_private', True),
        )
        collections = self.cleaned_data.get('collections')
        if collections:
            bookmark.collections.set(collections)
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
    collections = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Collection.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        label=_('Collections'),
    )

    class Meta:
        model = Bookmark
        fields = ('note', 'is_private')
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial['tag_names'] = ', '.join(
                self.instance.tags.values_list('name', flat=True),
            )
            self.fields['collections'].queryset = (
                Collection.objects.filter(user=self.instance.user)
                .order_by('position', 'name')
            )
            self.initial['collections'] = self.instance.collections.all()

    def save(self, commit=True):
        bookmark = super().save(commit=False)
        from core.services.bookmark import render_note
        bookmark.note_html = render_note(bookmark.note)
        if commit:
            bookmark.save()
            self._save_tags(bookmark)
            collections = self.cleaned_data.get('collections')
            if collections is not None:
                bookmark.collections.set(collections)
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
