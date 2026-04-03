from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils import timezone
from django.views import View

from core.models import Bookmark, ReadingStatus

MAX_PINS = 10


# Status cycle: unread → read → archived → unread
STATUS_CYCLE = {
    ReadingStatus.UNREAD: ReadingStatus.READ,
    ReadingStatus.READ: ReadingStatus.ARCHIVED,
    ReadingStatus.ARCHIVED: ReadingStatus.UNREAD,
}


class BookmarkStatusToggleView(LoginRequiredMixin, View):
    """HTMX endpoint: cycle bookmark reading status."""

    def post(self, request, pk):
        bookmark = get_object_or_404(Bookmark, pk=pk, user=request.user)
        bookmark.status = STATUS_CYCLE.get(bookmark.status, ReadingStatus.UNREAD)
        bookmark.save(update_fields=['status'])

        return TemplateResponse(
            request,
            'partials/status_badge.html',
            {'bookmark': bookmark},
        )


class BookmarkPinToggleView(LoginRequiredMixin, View):
    """HTMX endpoint: toggle pin on a bookmark."""

    def post(self, request, pk):
        bookmark = get_object_or_404(Bookmark, pk=pk, user=request.user)

        if bookmark.is_pinned:
            bookmark.is_pinned = False
            bookmark.pinned_at = None
            bookmark.save(update_fields=['is_pinned', 'pinned_at'])
        else:
            pin_count = Bookmark.objects.filter(user=request.user, is_pinned=True).count()
            if pin_count >= MAX_PINS:
                return HttpResponse(
                    '<span class="pin-error">Max 10 pins</span>',
                    status=200,
                )
            bookmark.is_pinned = True
            bookmark.pinned_at = timezone.now()
            bookmark.save(update_fields=['is_pinned', 'pinned_at'])

        return TemplateResponse(
            request,
            'partials/pin_button.html',
            {'bookmark': bookmark},
        )


class BookmarkStatusSetView(LoginRequiredMixin, View):
    """HTMX endpoint: set bookmark to a specific status."""

    def post(self, request, pk, status):
        if status not in ReadingStatus.values:
            return HttpResponse(status=400)

        bookmark = get_object_or_404(Bookmark, pk=pk, user=request.user)
        bookmark.status = status
        bookmark.save(update_fields=['status'])

        return TemplateResponse(
            request,
            'partials/status_badge.html',
            {'bookmark': bookmark},
        )
