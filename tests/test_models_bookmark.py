from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from core.models import Bookmark, Link

User = get_user_model()


class BookmarkModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='saver', password='pass')
        self.link = Link.objects.create(url='https://example.com')

    def test_str(self):
        bm = Bookmark(user=self.user, link=self.link)
        self.assertIn('saved', str(bm))

    def test_unique_constraint(self):
        Bookmark.objects.create(user=self.user, link=self.link)
        with self.assertRaises(IntegrityError):
            Bookmark.objects.create(user=self.user, link=self.link)

    def test_parent_relationship(self):
        parent_bm = Bookmark.objects.create(user=self.user, link=self.link, note='original')
        other_user = User.objects.create_user(username='other', password='pass')
        child_bm = Bookmark.objects.create(user=other_user, link=self.link, parent=parent_bm)
        self.assertEqual(child_bm.parent, parent_bm)
