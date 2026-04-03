from django.db.models import F
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from core.models import Comment
from core.models.notification import NotificationType
from core.services.link import LinkService
from core.services.notification import NotificationService


@receiver(pre_save, sender=Comment)
def render_comment_markdown(sender, instance, **kwargs):
    if instance.body:
        instance.body_html = LinkService.render_markdown(instance.body)
    else:
        instance.body_html = ''


@receiver(post_save, sender=Comment)
def on_comment_created(sender, instance, created, **kwargs):
    if not created:
        return

    instance.link.__class__.objects.filter(pk=instance.link_id).update(
        comment_count=F('comment_count') + 1,
    )

    # notify all users who bookmarked this link (except the commenter)
    from django.contrib.auth import get_user_model

    User = get_user_model()
    bookmark_user_ids = instance.link.bookmarks.exclude(
        user=instance.posted_by,
    ).values_list('user_id', flat=True).distinct()

    for recipient in User.objects.filter(pk__in=bookmark_user_ids):
        NotificationService.create_notification(
            actor=instance.posted_by,
            recipient=recipient,
            notification_type=NotificationType.COMMENTED_YOUR_POST,
            target_link=instance.link,
            target_comment=instance,
        )


@receiver(post_delete, sender=Comment)
def on_comment_deleted(sender, instance, **kwargs):
    instance.link.__class__.objects.filter(pk=instance.link_id).update(
        comment_count=F('comment_count') - 1,
    )
