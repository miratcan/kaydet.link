from django.db import models
from django.utils.translation import gettext_lazy as _


class TagManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Tag(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('name'),
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name=_('slug'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at'),
    )

    objects = TagManager()

    class Meta:
        app_label = 'core'
        db_table = 'tag'
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}'

    def natural_key(self):
        return (self.slug,)

    def get_absolute_url(self):
        return f'/tag/{self.slug}/'
