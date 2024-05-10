from django.contrib.messages import get_messages
from django.http import HttpResponse

from users.models import UserModel


def flash_message_test(response, expected_message):
    number_message = 1
    current_message = get_messages(response.wsgi_request)
    assert len(current_message) == number_message
    assert str(*current_message) == expected_message


class TestMixin:
    """Test mixin."""

    user_id = None
    url = None

    @classmethod
    def setUpTestData(cls):
        """Set up data."""
        cls.user = UserModel.objects.get(pk=cls.user_id)

    def get_user_auth_response(
            self,
            user: UserModel = None,
            url: str = None,
    ) -> HttpResponse:
        """Return response with logged user."""
        user = user or self.user
        url = url or self.url
        if user:
            self.client.force_login(user)
        return self.client.get(url)

    def set_session(self, **data) -> None:
        """Save data to session."""
        session = self.client.session
        for key, value in data.items():
            session[key] = value
        session.save()

    @staticmethod
    def flash_message_test(response, expected_message):
        """Test displaying Django message."""
        number_message = 1
        current_message = get_messages(response.wsgi_request)
        assert len(current_message) == number_message
        assert str(*current_message) == expected_message
