from django.test import TestCase


class AuthViewsTest(TestCase):
    def test_login_page_200(self):
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
