from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class CommentManager(models.Manager):
    def get_by_natural_key(self, posted_by_username, link_title, created_at):
        return self.get(
            posted_by=get_user_model().objects.get_by_natural_key(posted_by_username),
            link__title=link_title,
            created_at=created_at,
        )


class Comment(models.Model):
    link = models.ForeignKey(
        to='core.Link',
        related_name='comments',
        related_query_name='comment',
        on_delete=models.CASCADE,
        verbose_name=_('link'),
    )
    posted_by = models.ForeignKey(
        to=get_user_model(),
        related_name='comments',
        related_query_name='comment',
        on_delete=models.CASCADE,
        verbose_name=_('posted by'),
    )
    body = models.TextField(
        verbose_name=_('body'),
    )
    body_html = models.TextField(
        blank=True,
        editable=False,
        verbose_name=_('body HTML'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('updated at'),
    )

    objects = CommentManager()

    class Meta:
        app_label = 'core'
        db_table = 'comment'
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.posted_by} on {self.link}'

    def natural_key(self):
        return (self.posted_by.username, self.link.title, self.created_at)

    natural_key.dependencies = ['auth.user', 'core.link']
