from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from core.forms.collection import CollectionForm
from core.models import Collection

User = get_user_model()


class CollectionListView(LoginRequiredMixin, ListView):
    template_name = 'collections/list.html'
    context_object_name = 'collections'

    def get_queryset(self):
        return (
            Collection.objects.filter(user=self.request.user)
            .annotate(bookmark_count=Count('bookmarks'))
            .order_by('position', 'name')
        )


class CollectionDetailView(ListView):
    template_name = 'collections/detail.html'
    context_object_name = 'bookmarks'
    paginate_by = 20

    def get_collection(self):
        if not hasattr(self, '_collection'):
            user = get_object_or_404(User, username=self.kwargs['username'])
            self._collection = get_object_or_404(
                Collection, user=user, slug=self.kwargs['slug'],
            )
        return self._collection

    def get_queryset(self):
        collection = self.get_collection()
        qs = collection.bookmarks.select_related('link', 'user').prefetch_related('tags')
        # If not the owner, only show public bookmarks in public collections
        if self.request.user != collection.user:
            if collection.is_private:
                return qs.none()
            qs = qs.filter(is_private=False)
        return qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection'] = self.get_collection()
        context['is_owner'] = (
            self.request.user.is_authenticated
            and self.request.user == self.get_collection().user
        )
        return context


class CollectionCreateView(LoginRequiredMixin, CreateView):
    template_name = 'collections/form.html'
    form_class = CollectionForm

    def form_valid(self, form):
        form.save(user=self.request.user)
        return redirect('collection-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'New Collection'
        return context


class CollectionEditView(LoginRequiredMixin, UpdateView):
    template_name = 'collections/form.html'
    form_class = CollectionForm

    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user)

    def get_object(self):
        return get_object_or_404(self.get_queryset(), slug=self.kwargs['slug'])

    def form_valid(self, form):
        form.save(user=self.request.user)
        return redirect('collection-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Collection'
        return context


class CollectionDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'collections/delete.html'

    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user)

    def get_object(self):
        return get_object_or_404(self.get_queryset(), slug=self.kwargs['slug'])

    def get_success_url(self):
        return '/collections/'


class CollectionAddBookmarkView(LoginRequiredMixin, CreateView):
    """HTMX endpoint to add/remove a bookmark from a collection."""
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        from core.models import Bookmark

        collection = get_object_or_404(
            Collection, user=request.user, pk=kwargs['collection_pk'],
        )
        bookmark = get_object_or_404(
            Bookmark, user=request.user, pk=kwargs['bookmark_pk'],
        )

        if collection.bookmarks.filter(pk=bookmark.pk).exists():
            collection.bookmarks.remove(bookmark)
        else:
            collection.bookmarks.add(bookmark)

        return redirect(request.META.get('HTTP_REFERER', '/'))
