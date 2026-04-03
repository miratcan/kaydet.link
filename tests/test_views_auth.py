from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class AuthViewsTest(TestCase):
    def test_login_page_200(self):
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)

    def test_register_page_200(self):
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, 200)

    def test_register_creates_user(self):
        response = self.client.post('/auth/register/', {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_works(self):
        User.objects.create_user(username='logintest', password='TestPass123!')
        response = self.client.post('/auth/login/', {
            'username': 'logintest',
            'password': 'TestPass123!',
        })
        self.assertEqual(response.status_code, 302)
