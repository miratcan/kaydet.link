from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import CreateView, UpdateView

from core.forms.comment import CommentForm
from core.models import Comment, Link


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments/partials/form.html'

    def form_valid(self, form):
        link = get_object_or_404(Link, pk=self.kwargs.get('link_pk'))
        form.instance.posted_by = self.request.user
        form.instance.link = link
        form.save()
        return redirect(link.get_absolute_url())

    def form_invalid(self, form):
        link = get_object_or_404(Link, pk=self.kwargs.get('link_pk'))
        return redirect(link.get_absolute_url())


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments/partials/form.html'

    def get_queryset(self):
        return Comment.objects.filter(posted_by=self.request.user)

    def get_success_url(self):
        return self.object.link.get_absolute_url()


class CommentDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.posted_by != request.user:
            return HttpResponseForbidden()
        link_url = comment.link.get_absolute_url()
        comment.delete()
        return redirect(link_url)
