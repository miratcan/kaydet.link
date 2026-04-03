from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from core.forms.preferences import UpdatePreferencesForm
from core.models import UserPreferences


class PreferencesUpdateView(LoginRequiredMixin, UpdateView):
    model = UserPreferences
    form_class = UpdatePreferencesForm
    template_name = 'preferences/update.html'
    success_url = reverse_lazy('preferences')

    def get_object(self, queryset=None):
        obj, _created = UserPreferences.objects.get_or_create(
            user=self.request.user,
        )
        return obj
