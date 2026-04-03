from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import Bookmark, Link, Tag

User = get_user_model()


class LinkViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.tag = Tag.objects.create(name='python', slug='python')
        self.link = Link.objects.create(
            url='https://example.com',
            metadata={'og:title': 'Test Link'},
        )
        self.bookmark = Bookmark.objects.create(
            user=self.user,
            link=self.link,
            note='test note',
        )
        self.bookmark.tags.add(self.tag)

    def test_link_list_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_link_list_by_tag_200(self):
        response = self.client.get(f'/tag/{self.tag.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_link_list_by_user_200(self):
        response = self.client.get(f'/user/{self.user.username}/')
        self.assertEqual(response.status_code, 200)

    def test_link_detail_200(self):
        response = self.client.get(f'/links/{self.link.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_bookmark_create_requires_login(self):
        response = self.client.get('/bookmarks/new/')
        self.assertEqual(response.status_code, 302)

    def test_bookmark_create_logged_in(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get('/bookmarks/new/')
        self.assertEqual(response.status_code, 200)

    def test_bookmark_create_post(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post('/bookmarks/new/', {
            'url': 'https://new.example.com',
            'note': 'cool link',
            'tag_names': 'python, django',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Link.objects.filter(url='https://new.example.com').exists())

    def test_random_redirects(self):
        response = self.client.get('/links/random/')
        self.assertEqual(response.status_code, 302)

    def test_tag_list_200(self):
        response = self.client.get('/tags/')
        self.assertEqual(response.status_code, 200)
