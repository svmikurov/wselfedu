"""Test auth user module."""

from django.contrib import auth
from django.urls import reverse_lazy

from contrib.tests_extension import UserAuthTestCase


class TestAuthUser(UserAuthTestCase):
    """Auth user test."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up test data."""
        super().setUpClass()
        cls.login_url = reverse_lazy('users:login')
        cls.logout_url = reverse_lazy('users:logout')
        cls.redirect_url = reverse_lazy('home')
        cls.user_data = {'username': 'user', 'password': '1q2s3d4r'}
        cls.wrong_user_data = {
            'username': 'user',
            'password': 'wrong-password',
        }

    def test_login_get_method(self) -> None:
        """Test the http status of render the login form."""
        response = self.client.get(self.login_url)
        self.assertTrue(response.status_code, 200)

    def test_login_post_method(self) -> None:
        """Test the http status of submit the login form."""
        response = self.client.post(self.login_url, self.user_data)
        user = auth.get_user(self.client)

        self.assertRedirects(response, self.redirect_url, 302)
        self.assertMessage(response, 'Вы вошли в приложение')
        self.assertTrue(user.is_authenticated)

    def test_wrong_password_login(self) -> None:
        """Test the login with wrong password."""
        self.client.post(self.login_url, self.wrong_user_data)
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout(self) -> None:
        """Test logout."""
        response = self.get_auth_response(self.logout_url, method='post')
        user = auth.get_user(self.client)

        self.assertRedirects(response, self.redirect_url, 302)
        self.assertMessage(response, 'Вы вышли из приложения')
        self.assertFalse(user.is_authenticated)
