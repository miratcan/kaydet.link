from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class Collection(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_('name'),
    )
    slug = models.SlugField(
        max_length=100,
        verbose_name=_('slug'),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('description'),
    )
    user = models.ForeignKey(
        to=get_user_model(),
        related_name='collections',
        related_query_name='collection',
        on_delete=models.CASCADE,
        verbose_name=_('user'),
    )
    is_private = models.BooleanField(
        default=True,
        verbose_name=_('private'),
        help_text=_('Only you can see this collection'),
    )
    position = models.IntegerField(
        default=0,
        verbose_name=_('position'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('updated at'),
    )

    class Meta:
        app_label = 'core'
        db_table = 'collection'
        verbose_name = _('Collection')
        verbose_name_plural = _('Collections')
        ordering = ('position', 'name')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'slug'],
                name='uc_collection_user_slug',
            ),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/collections/{self.user.username}/{self.slug}/'
