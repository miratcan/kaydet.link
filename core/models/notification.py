from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationType(models.TextChoices):
    SAVED_YOUR_LINK = 'saved_your_link', _('saved your link')
    COMMENTED_YOUR_POST = 'commented_your_post', _('commented on your post')


class Notification(models.Model):
    actor = models.ForeignKey(
        to=get_user_model(),
        related_name='notifications_sent',
        related_query_name='notification_sent',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_('actor'),
    )
    recipient = models.ForeignKey(
        to=get_user_model(),
        related_name='notifications_received',
        related_query_name='notification_received',
        on_delete=models.CASCADE,
        verbose_name=_('recipient'),
    )
    type = models.CharField(
        max_length=32,
        choices=NotificationType.choices,
        verbose_name=_('type'),
    )
    target_link = models.ForeignKey(
        to='core.Link',
        related_name='notifications',
        related_query_name='notification',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_('target link'),
    )
    target_comment = models.ForeignKey(
        to='core.Comment',
        related_name='notifications',
        related_query_name='notification',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_('target comment'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at'),
    )
    seen = models.BooleanField(
        default=False,
        verbose_name=_('seen'),
    )

    class Meta:
        app_label = 'core'
        db_table = 'notification'
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.actor} {self.get_type_display()} → {self.recipient}'
