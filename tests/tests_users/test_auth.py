from django.contrib import auth
from django.test import TestCase
from django.urls import reverse_lazy

from contrib.mixins_tests import UserAuthTestMixin


class TestAuthUser(UserAuthTestMixin, TestCase):
    """Auth user test."""

    @classmethod
    def setUpClass(cls):
        """Set up test data."""
        super().setUpClass()
        cls.login_url = reverse_lazy('users:login')
        cls.logout_url = reverse_lazy('users:logout')
        cls.redirect_url = reverse_lazy('home')
        cls.user_data = {'username': 'user', 'password': '1q2s3d4r'}

    def test_login_get_method(self):
        """Test login get method."""
        response = self.client.get(self.login_url)
        self.assertTrue(response.status_code, 200)

    def test_login_post_method(self):
        """Test login post method."""
        response = self.client.post(self.login_url, self.user_data)
        user = auth.get_user(self.client)

        self.assertRedirects(response, self.redirect_url, 302)
        self.assertMessage(response, 'Вы вошли в приложение')
        self.assertTrue(user.is_authenticated)

    def test_logout(self):
        """Test logout."""
        response = self.get_auth_response(url=self.logout_url, method='post')
        user = auth.get_user(self.client)

        self.assertRedirects(response, self.redirect_url, 302)
        self.assertMessage(response, 'Вы вышли из приложения')
        self.assertFalse(user.is_authenticated)
