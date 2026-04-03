from django import forms
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from core.models import Collection


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ('name', 'description', 'is_private')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _('e.g. Django Resources')}),
            'description': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': _('What is this collection about?'),
            }),
        }

    def save(self, user=None, commit=True):
        collection = super().save(commit=False)
        if user:
            collection.user = user
        collection.slug = slugify(collection.name, allow_unicode=True)
        # Ensure slug uniqueness per user
        base_slug = collection.slug
        counter = 1
        while Collection.objects.filter(
            user=collection.user, slug=collection.slug,
        ).exclude(pk=collection.pk).exists():
            collection.slug = f'{base_slug}-{counter}'
            counter += 1
        if commit:
            collection.save()
        return collection
