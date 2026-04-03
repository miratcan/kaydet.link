from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class BookmarkManager(models.Manager):
    def get_by_natural_key(self, username, url):
        return self.get(
            user=get_user_model().objects.get_by_natural_key(username),
            link__url=url,
        )


class Bookmark(models.Model):
    user = models.ForeignKey(
        to=get_user_model(),
        related_name='bookmarks',
        related_query_name='bookmark',
        on_delete=models.CASCADE,
        verbose_name=_('user'),
    )
    link = models.ForeignKey(
        to='core.Link',
        related_name='bookmarks',
        related_query_name='bookmark',
        on_delete=models.CASCADE,
        verbose_name=_('link'),
    )
    parent = models.ForeignKey(
        to='self',
        related_name='saves',
        related_query_name='save',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('saved from'),
    )
    note = models.TextField(
        blank=True,
        verbose_name=_('note'),
    )
    note_html = models.TextField(
        blank=True,
        editable=False,
        verbose_name=_('note HTML'),
    )
    tags = models.ManyToManyField(
        to='core.Tag',
        related_name='bookmarks',
        blank=True,
        verbose_name=_('tags'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at'),
    )

    objects = BookmarkManager()

    class Meta:
        app_label = 'core'
        db_table = 'bookmark'
        verbose_name = _('Bookmark')
        verbose_name_plural = _('Bookmarks')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'link'],
                name='uc_bookmark_user_link',
            ),
        ]

    def __str__(self):
        return f'{self.user} saved {self.link}'

    def natural_key(self):
        return (self.user.username, self.link.url)

    natural_key.dependencies = ['auth.user', 'core.link']
