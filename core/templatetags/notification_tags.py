from django import template

register = template.Library()


@register.simple_tag
def get_unread_count(user):
    if not user.is_authenticated:
        return 0
    from core.services.notification import NotificationService

    return NotificationService.unread_count(user)
