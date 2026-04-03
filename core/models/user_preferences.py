from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class SummaryFrequency(models.TextChoices):
    DAILY = 'daily', _('Daily')
    WEEKLY = 'weekly', _('Weekly')
    NEVER = 'never', _('Never')


class UserPreferencesManager(models.Manager):
    def get_by_natural_key(self, username):
        return self.get(
            user=get_user_model().objects.get_by_natural_key(username),
        )


class UserPreferences(models.Model):
    user = models.OneToOneField(
        to=get_user_model(),
        related_name='preferences',
        on_delete=models.CASCADE,
        verbose_name=_('user'),
    )
    bio = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('bio'),
    )
    summary_mails = models.CharField(
        max_length=10,
        choices=SummaryFrequency.choices,
        default=SummaryFrequency.NEVER,
        verbose_name=_('summary emails'),
    )

    objects = UserPreferencesManager()

    class Meta:
        app_label = 'core'
        db_table = 'user_preferences'
        verbose_name = _('User Preferences')
        verbose_name_plural = _('User Preferences')

    def __str__(self):
        return f'{self.user} preferences'

    def natural_key(self):
        return (self.user.username,)

    natural_key.dependencies = ['auth.user']
