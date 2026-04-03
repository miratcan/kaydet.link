from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from core.models import Notification
from core.services.notification import NotificationService


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications/list.html'
    context_object_name = 'notifications'
    paginate_by = 30

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user,
        ).select_related('actor', 'target_link', 'target_comment')

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        NotificationService.mark_as_read(request.user)
        return response
