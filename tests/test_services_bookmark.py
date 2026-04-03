from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import Bookmark, Link
from core.services.bookmark import BookmarkService

User = get_user_model()


class BookmarkServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='saver', password='pass')
        self.link = Link.objects.create(url='https://example.com')

    def test_create_bookmark(self):
        bm = BookmarkService.create_bookmark(self.user, 'https://example.com', note='great link')
        self.assertEqual(bm.link, self.link)
        self.assertEqual(bm.note, 'great link')
        self.link.refresh_from_db()
        self.assertEqual(self.link.save_count, 1)

    def test_create_bookmark_new_url(self):
        bm = BookmarkService.create_bookmark(self.user, 'https://new.example.com')
        self.assertEqual(bm.link.url, 'https://new.example.com')
        self.assertTrue(Link.objects.filter(url='https://new.example.com').exists())

    def test_save_from_parent(self):
        parent_bm = Bookmark.objects.create(user=self.user, link=self.link, note='original note')
        other_user = User.objects.create_user(username='other', password='pass')
        child_bm = BookmarkService.save_from(other_user, parent_bm)
        self.assertEqual(child_bm.parent, parent_bm)
        self.assertEqual(child_bm.note, 'original note')
        self.assertEqual(child_bm.link, self.link)

    def test_is_saved(self):
        self.assertFalse(BookmarkService.is_saved(self.user, self.link))
        Bookmark.objects.create(user=self.user, link=self.link)
        self.assertTrue(BookmarkService.is_saved(self.user, self.link))
