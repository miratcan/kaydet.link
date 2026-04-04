from django.db import models
from django.utils.translation import gettext_lazy as _


class LinkManager(models.Manager):
    def get_by_natural_key(self, url):
        return self.get(url=url)


class Link(models.Model):
    url = models.URLField(
        max_length=2000,
        unique=True,
        verbose_name=_('URL'),
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('page metadata'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at'),
    )
    save_count = models.IntegerField(
        default=0,
        editable=False,
        verbose_name=_('save count'),
    )
    comment_count = models.IntegerField(
        default=0,
        editable=False,
        verbose_name=_('comment count'),
    )
    last_saved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('last saved at'),
    )

    objects = LinkManager()

    class Meta:
        app_label = 'core'
        db_table = 'link'
        verbose_name = _('Link')
        verbose_name_plural = _('Links')
        ordering = ('-last_saved_at', '-created_at')

    def __str__(self):
        return self.title or self.url

    def natural_key(self):
        return (self.url,)

    def get_absolute_url(self):
        return f'/links/{self.pk}/'

    def get_domain(self):
        from urllib.parse import urlparse

        return urlparse(self.url).netloc

    @property
    def title(self):
        return self.metadata.get('og:title', '')

    @property
    def description(self):
        return self.metadata.get('og:description', '')

    @property
    def image(self):
        return self.metadata.get('og:image', '')

    @property
    def first_bookmark(self):
        return self.bookmarks.order_by('created_at').first()

    @property
    def top_tags(self):
        from core.models import Tag

        return (
            Tag.objects.filter(bookmarks__link=self)
            .annotate(usage_count=models.Count('id'))
            .order_by('-usage_count')[:3]
        )
