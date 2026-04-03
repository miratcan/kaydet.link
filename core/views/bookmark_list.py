from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from core.models import Bookmark, ReadingStatus


class BookmarkListView(LoginRequiredMixin, ListView):
    template_name = 'bookmarks/list.html'
    context_object_name = 'bookmarks'
    paginate_by = 20

    def get_queryset(self):
        qs = (
            Bookmark.objects.filter(user=self.request.user)
            .select_related('link')
            .prefetch_related('tags')
            .order_by('-created_at')
        )
        status = self.request.GET.get('status')
        if status in ReadingStatus.values:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', '')
        context['statuses'] = ReadingStatus.choices
        return context
