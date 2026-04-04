from django.db.models import BooleanField, Count, Exists, OuterRef, Q, Value
from django.views.generic import ListView

from core.models import Bookmark, Link, Tag


class SearchView(ListView):
    template_name = 'search/results.html'
    context_object_name = 'links'
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        scope = self.request.GET.get('scope', 'mine')
        user = self.request.user

        if not query:
            return Link.objects.none()

        # Build search filter across Link metadata + Bookmark note + Tag name + URL
        q_filter = (
            Q(metadata__icontains=query)
            | Q(url__icontains=query)
            | Q(bookmark__note__icontains=query)
            | Q(bookmark__tags__name__icontains=query)
        )

        qs = Link.objects.filter(q_filter).distinct()

        if user.is_authenticated and scope == 'mine':
            # Only show links the user has bookmarked
            qs = qs.filter(bookmark__user=user)
        elif user.is_authenticated:
            # All platform: show links with public bookmarks or user's own
            qs = qs.filter(
                Q(bookmark__is_private=False) | Q(bookmark__user=user),
            )
        else:
            # Unauthenticated: only public
            qs = qs.filter(bookmark__is_private=False)

        # Annotate user bookmark status
        if user.is_authenticated:
            qs = qs.annotate(
                is_saved=Exists(
                    Bookmark.objects.filter(user=user, link=OuterRef('pk')),
                ),
            )
        else:
            qs = qs.annotate(is_saved=Value(False, output_field=BooleanField()))

        return qs.prefetch_related('bookmarks__tags').order_by('-last_saved_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['scope'] = self.request.GET.get('scope', 'mine')
        if not context['query']:
            context['popular_tags'] = (
                Tag.objects.annotate(usage_count=Count('bookmarks'))
                .filter(usage_count__gt=0)
                .order_by('-usage_count')[:12]
            )
        return context
