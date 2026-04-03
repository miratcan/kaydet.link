from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class PageManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Page(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('name'),
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name=_('slug'),
    )
    content = models.TextField(
        blank=True,
        verbose_name=_('content'),
    )
    content_html = models.TextField(
        blank=True,
        editable=False,
        verbose_name=_('content HTML'),
    )
    is_listed = models.BooleanField(
        default=True,
        verbose_name=_('is listed'),
    )
    contributors = models.ManyToManyField(
        to=get_user_model(),
        related_name='wiki_contributions',
        blank=True,
        verbose_name=_('contributors'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('updated at'),
    )

    objects = PageManager()

    class Meta:
        app_label = 'core'
        db_table = 'wiki_page'
        verbose_name = _('Wiki Page')
        verbose_name_plural = _('Wiki Pages')
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'

    def natural_key(self):
        return (self.slug,)

    def get_absolute_url(self):
        return f'/wiki/{self.slug}/'
