from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.forms.auth import RegistrationForm


class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('link-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
