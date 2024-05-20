from typing import Any

from django.contrib.messages import get_messages
from django.http import HttpResponse

from users.models import UserModel


def flash_message_test(response, expected_message):
    """Test displaying Django message."""
    number_message = 1
    current_message = get_messages(response.wsgi_request)
    assert len(current_message) == number_message
    assert str(*current_message) == expected_message


class UserAuthTestMixin:
    """Test mixin."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        cls.user = UserModel.objects.create_user(
            username='user',
            password='1q2s3d4r',
        )

    def get_auth_response(
            self,
            url: str = None,
            user: UserModel = None,
            method: str = 'get',
            **kwargs: Any,
    ) -> HttpResponse:
        """Return response with logged user.

        Parameters:
        -----------
        user : `UserModel`
            User for login (default is class attribute value).
        url : `str`
            Page url (default is class attribute value).
        """
        user = user or self.user
        url = url or self.url
        if not url:
            raise AttributeError('Set the `url` attribute value')
        self.client.force_login(user)

        if method == 'post':
            return self.client.post(url, kwargs)
        return self.client.get(url)

    def set_session(self, **data) -> None:
        """Save data to session."""
        session = self.client.session
        for key, value in data.items():
            session[key] = value
        session.save()

    @staticmethod
    def assertMessage(response, expected_message):
        """Test displaying Django message."""
        return flash_message_test(response, expected_message)


class TestMixin:
    """Test mixin."""

    user_id = None
    url = None

    @classmethod
    def setUpTestData(cls):
        """Set up data."""
        if not cls.user_id:
            raise AttributeError('Set the logged `user_id` attribute value')
        cls.user = UserModel.objects.get(pk=cls.user_id)

    def get_user_auth_response(
            self,
            user: UserModel = None,
            url: str = None,
    ) -> HttpResponse:
        """Return response with logged user.

        Parameters:
        -----------
        user : `UserModel`
            User for login (default is class attribute value).
        url : `str`
            Page url (default is class attribute value).
        """
        if not self.url:
            raise AttributeError('Set the `url` attribute value')
        user = user or self.user
        url = url or self.url
        self.client.force_login(user)
        return self.client.get(url)

    def set_session(self, **data) -> None:
        """Save data to session."""
        session = self.client.session
        for key, value in data.items():
            session[key] = value
        session.save()

    @staticmethod
    def assertMessage(response, expected_message):
        """Test displaying Django message."""
        return flash_message_test(response, expected_message)
