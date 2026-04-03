from django.test import TestCase

from core.models import Tag


class TagModelTest(TestCase):
    def test_str_returns_name(self):
        tag = Tag(name='python', slug='python')
        self.assertEqual(str(tag), 'python')

    def test_natural_key(self):
        tag = Tag.objects.create(name='django', slug='django')
        self.assertEqual(tag.natural_key(), ('django',))

    def test_get_by_natural_key(self):
        tag = Tag.objects.create(name='rust', slug='rust')
        found = Tag.objects.get_by_natural_key('rust')
        self.assertEqual(found.pk, tag.pk)

    def test_get_absolute_url(self):
        tag = Tag(name='web', slug='web')
        self.assertEqual(tag.get_absolute_url(), '/tag/web/')
