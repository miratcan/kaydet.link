from django.db.models import Count
from django.views.generic import ListView

from core.models import Tag

MIN_FONT = 0.75
MAX_FONT = 2.0


class TagListView(ListView):
    model = Tag
    template_name = 'tags/list.html'
    context_object_name = 'tags'

    def get_queryset(self):
        return Tag.objects.annotate(
            usage_count=Count('bookmarks'),
        ).filter(usage_count__gt=0).order_by('-usage_count', 'name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = list(context['tags'])
        if tags:
            counts = [t.usage_count for t in tags]
            min_c, max_c = min(counts), max(counts)
            spread = max_c - min_c or 1
            for tag in tags:
                tag.font_size = MIN_FONT + (MAX_FONT - MIN_FONT) * (tag.usage_count - min_c) / spread
        context['tags'] = tags
        return context
