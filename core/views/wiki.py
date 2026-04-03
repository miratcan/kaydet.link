from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView, UpdateView

from core.models import Page


class WikiIndexView(ListView):
    model = Page
    template_name = 'wiki/index.html'
    context_object_name = 'pages'

    def get_queryset(self):
        return Page.objects.filter(is_listed=True)


class WikiPageView(DetailView):
    model = Page
    template_name = 'wiki/view.html'
    context_object_name = 'page'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class WikiEditView(LoginRequiredMixin, UpdateView):
    model = Page
    template_name = 'wiki/edit.html'
    fields = ('name', 'content', 'is_listed')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        page = form.save()
        page.contributors.add(self.request.user)
        return redirect(page.get_absolute_url())
