from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from core.models import Bookmark
from core.models.notification import NotificationType
from core.services.link import LinkService
from core.services.notification import NotificationService


@receiver(pre_save, sender=Bookmark)
def render_bookmark_markdown(sender, instance, **kwargs):
    if instance.note:
        instance.note_html = LinkService.render_markdown(instance.note)
    else:
        instance.note_html = ''


@receiver(post_save, sender=Bookmark)
def on_bookmark_saved(sender, instance, created, **kwargs):
    if created:
        link = instance.link
        link.save_count = link.bookmarks.filter(is_private=False).count()
        link.last_saved_at = timezone.now()
        link.save(update_fields=['save_count', 'last_saved_at'])

        # notify the first person who bookmarked this link
        first_bookmark = link.bookmarks.order_by('created_at').first()
        if first_bookmark and first_bookmark.user != instance.user:
            NotificationService.create_notification(
                actor=instance.user,
                recipient=first_bookmark.user,
                notification_type=NotificationType.SAVED_YOUR_LINK,
                target_link=link,
            )


@receiver(post_delete, sender=Bookmark)
def on_bookmark_deleted(sender, instance, **kwargs):
    link = instance.link
    link.save_count = link.bookmarks.filter(is_private=False).count()
    link.save(update_fields=['save_count'])
