from django.views.generic import ListView

from core.models import Tag


class TagListView(ListView):
    model = Tag
    template_name = 'tags/list.html'
    context_object_name = 'tags'

    def get_queryset(self):
        return Tag.objects.all().order_by('name')
