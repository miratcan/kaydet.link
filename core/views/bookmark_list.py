from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from core.models import Bookmark


class BookmarkListView(LoginRequiredMixin, ListView):
    template_name = 'bookmarks/list.html'
    context_object_name = 'bookmarks'
    paginate_by = 20

    def get_queryset(self):
        return (
            Bookmark.objects.filter(user=self.request.user)
            .select_related('link')
            .prefetch_related('tags')
            .order_by('-created_at')
        )
