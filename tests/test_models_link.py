from django.test import TestCase

from core.models import Link


class LinkModelTest(TestCase):
    def test_str_returns_title_from_metadata(self):
        link = Link(url='https://example.com', metadata={'og:title': 'Hello World'})
        self.assertEqual(str(link), 'Hello World')

    def test_str_falls_back_to_url(self):
        link = Link(url='https://example.com', metadata={})
        self.assertEqual(str(link), 'https://example.com')

    def test_title_property(self):
        link = Link(metadata={'og:title': 'Test Title'})
        self.assertEqual(link.title, 'Test Title')

    def test_description_property(self):
        link = Link(metadata={'og:description': 'A desc'})
        self.assertEqual(link.description, 'A desc')

    def test_image_property(self):
        link = Link(metadata={'og:image': 'https://img.example.com/pic.png'})
        self.assertEqual(link.image, 'https://img.example.com/pic.png')

    def test_get_domain(self):
        link = Link(url='https://example.com/foo/bar')
        self.assertEqual(link.get_domain(), 'example.com')

    def test_get_absolute_url(self):
        link = Link.objects.create(url='https://example.com')
        self.assertEqual(link.get_absolute_url(), f'/links/{link.pk}/')

    def test_natural_key(self):
        link = Link.objects.create(url='https://example.com/my-link')
        self.assertEqual(link.natural_key(), ('https://example.com/my-link',))

    def test_url_unique(self):
        Link.objects.create(url='https://example.com')
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Link.objects.create(url='https://example.com')
