from django import forms

from core.models import UserPreferences


class UpdatePreferencesForm(forms.ModelForm):
    class Meta:
        model = UserPreferences
        fields = ('bio', 'summary_mails')
