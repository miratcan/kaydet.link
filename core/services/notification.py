import logging

from core.exceptions import NotificationServiceError

logger = logging.getLogger('core.NotificationService')


class NotificationService:

    @staticmethod
    def create_notification(actor, recipient, notification_type, target_link=None, target_comment=None):
        from core.models import Notification

        if actor == recipient:
            return None

        try:
            return Notification.objects.create(
                actor=actor,
                recipient=recipient,
                type=notification_type,
                target_link=target_link,
                target_comment=target_comment,
            )
        except Exception as exc:
            logger.exception('Failed to create notification')
            raise NotificationServiceError('Could not create notification') from exc

    @staticmethod
    def mark_as_read(user):
        from core.models import Notification

        return Notification.objects.filter(
            recipient=user,
            seen=False,
        ).update(seen=True)

    @staticmethod
    def unread_count(user):
        from core.models import Notification

        return Notification.objects.filter(
            recipient=user,
            seen=False,
        ).count()
