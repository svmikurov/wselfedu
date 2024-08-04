"""Django tests extension module."""

from typing import TYPE_CHECKING

from django.contrib.messages import get_messages
from django.db.models import Model
from django.test import TestCase

from users.models import UserModel

if TYPE_CHECKING:
    from django.test.client import (
        _MonkeyPatchedWSGIResponse as TestHttpResponse,
    )


def flash_message_test(
    response: 'TestHttpResponse',
    expected_message: str,
) -> None:
    """Test displaying Django message.

    Parameters
    ----------
    response : `TestHttpResponse`
        Test http response.
    expected_message : `str`
        Expected message in response.
    """
    number_of_message = 1
    current_message = get_messages(response.wsgi_request)
    assert len(current_message) == number_of_message
    assert str(*current_message) == expected_message


class UserAuthTestCase(TestCase):
    """Authorized page test class.

    Inherit your test class from this.

    Extends the django.test.TestCase class by adding a user, a method
    to get an authorized response, a method to add data to a session,
    and a Django message test method.

    Examples
    --------
    .. code-block:: python

        class TestUpdateUserView(UserAuthTestMixin):

            @classmethod
            def setUpTestData(cls):
                super().setUpTestData()
                cls.path_schema = reverse(
                    'users:update',
                    kwargs={'pk': cls.user.id},
                )
                cls.update_user_data = {
                    'username': 'update_user',
                    'password1': '1q2s3d4r',
                    'password2': '1q2s3d4r',
                }

            def test_is_auth_response(self):
                response = self.get_auth_response()
                self.assertEqual(response.wsgi_request.user, self.user)

            def test_update_user(self):
                response = self.get_auth_response(
                    path_schema=self.path_schema,
                    method='post',
                    **self.update_user_data,
                )
                self.assertRedirects(
                    response, SUCCESS_REDIRECT_PATH, 302,
                )
                assert (UserModel.objects.filter(
                    username='update_user').exists())
    """

    path_schema = '/'
    """Page path schema (`str`).
    """
    user = None
    """User Django model instance (`Model`).
    """

    @classmethod
    def setUpTestData(cls) -> None:
        """Add user to database."""
        super().setUpTestData()
        cls.user = UserModel.objects.create_user(
            username='user',
            password='1q2s3d4r',
        )

    def get_auth_response(
        self,
        path_schema: str | None = None,
        user: Model | None = None,
        method: str = 'get',
        **kwargs: object,
    ) -> 'TestHttpResponse':
        """Get response with logged user.

        Parameters
        ----------
        path_schema : `str` | None
            Page path schema (default is class attribute value).
        user : `Model` | None
            User for login (default is class attribute value).
        method : `str`
            A HTML request method ('get', by default).
        kwargs: object
            Arbitrary keyword arguments.

        Returns
        -------
        `TestHttpResponse`
            Test http response.
        """
        user = user or self.user
        path_schema = path_schema or self.path_schema

        if not path_schema:
            raise AttributeError('Set the `url` attribute value')
        self.client.force_login(user)  # type: ignore[arg-type]

        if method == 'post':
            return self.client.post(path_schema, kwargs)
        return self.client.get(path_schema)

    def set_session(self, **data: dict[str, object]) -> None:
        """Save data to session.

        Parameters
        ----------
        data : `dict[str, object]`
            Arbitrary keyword arguments.

        Examples
        --------
        def test(self):
            task_conditions = {'timeout': 1, 'language_order': 'EN'}
            self.set_session(**{'task_conditions': task_conditions})
            ...
        """
        session = self.client.session
        for key, value in data.items():
            session[key] = value
        session.save()

    @staticmethod
    def assertMessage(  # noqa: N802
        response: 'TestHttpResponse',
        expected_message: str,
    ) -> None:
        """Test displaying Django message.

        Parameters
        ----------
        response : `TestHttpResponse`
            Test http response.
        expected_message : `str`
            Expected message in response.

        Examples
        --------
        def test(self):
            response = self.client.get(self.login_url, self.user_data)
            user = auth.get_user(self.client)
            ...
            self.assertMessage(response, 'Message text')
        """
        return flash_message_test(response, expected_message)
