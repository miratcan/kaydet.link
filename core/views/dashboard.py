from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from core.models import Bookmark, Collection, ReadingStatus, Tag


class HomeRedirectView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return redirect('link-list')


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        now = timezone.now()

        user_bookmarks = Bookmark.objects.filter(user=user).select_related('link')

        # Pinned bookmarks
        pinned_qs = (
            user_bookmarks
            .filter(is_pinned=True)
            .prefetch_related('tags')
            .order_by('-pinned_at')
        )
        context['pinned_bookmarks'] = pinned_qs
        pinned_ids = set(pinned_qs.values_list('pk', flat=True))

        # Unread bookmarks (to-read list), exclude pinned
        unread_qs = (
            user_bookmarks
            .filter(status=ReadingStatus.UNREAD)
            .exclude(pk__in=pinned_ids)
            .prefetch_related('tags')
            .order_by('-created_at')[:5]
        )
        context['unread_bookmarks'] = unread_qs
        shown_ids = pinned_ids | set(unread_qs.values_list('pk', flat=True))

        # Recent bookmarks (last 10), exclude already shown
        context['recent_bookmarks'] = (
            user_bookmarks
            .exclude(pk__in=shown_ids)
            .prefetch_related('tags')
            .order_by('-created_at')[:10]
        )

        # Collections
        context['collections'] = (
            Collection.objects.filter(user=user)
            .annotate(bookmark_count=Count('bookmarks'))
            .order_by('position', 'name')[:10]
        )

        # Top tags (most used by this user)
        context['top_tags'] = (
            Tag.objects
            .filter(bookmarks__user=user)
            .annotate(usage_count=Count('bookmarks'))
            .order_by('-usage_count')[:15]
        )

        # Stats
        context['stats'] = {
            'total': user_bookmarks.count(),
            'this_week': user_bookmarks.filter(
                created_at__gte=now - timedelta(days=7),
            ).count(),
            'unread_count': user_bookmarks.filter(status=ReadingStatus.UNREAD).count(),
            'private_count': user_bookmarks.filter(is_private=True).count(),
            'public_count': user_bookmarks.filter(is_private=False).count(),
        }

        # This day in history — check 3mo, 6mo, 1yr windows
        history_bookmarks = []
        for days_ago, label in [(90, '3 months'), (180, '6 months'), (365, '1 year')]:
            target = now - timedelta(days=days_ago)
            found = list(
                user_bookmarks
                .filter(
                    created_at__date__gte=(target - timedelta(days=1)).date(),
                    created_at__date__lte=(target + timedelta(days=1)).date(),
                )
                .prefetch_related('tags')
                .order_by('-created_at')[:3]
            )
            if found:
                history_bookmarks.append({'label': label, 'bookmarks': found})
        context['history_sections'] = history_bookmarks

        # Forgotten bookmark — random pick from user's bookmarks (older than 30 days)
        old_bookmarks = user_bookmarks.filter(
            created_at__lte=now - timedelta(days=30),
        )
        context['random_bookmark'] = old_bookmarks.order_by('?').first()

        return context


class DashboardRediscoverView(LoginRequiredMixin, View):
    def get(self, request):
        now = timezone.now()
        random_bookmark = (
            Bookmark.objects.filter(
                user=request.user,
                created_at__lte=now - timedelta(days=30),
            )
            .select_related('link')
            .order_by('?')
            .first()
        )
        return TemplateResponse(
            request,
            'dashboard/partials/rediscover.html',
            {'random_bookmark': random_bookmark},
        )
