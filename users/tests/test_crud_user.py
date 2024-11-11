"""The user management tests."""

from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse, reverse_lazy

from contrib.tests.extension import UserAuthTestCase, flash_message_test
from users.models import UserApp

NO_PERMISSION_MSG = 'Для доступа необходимо войти в приложение'
NO_PERMISSION_URL = reverse('users:login')
SUCCESS_REDIRECT_PATH = '/users/login/'


class TestCreateUserView(TestCase):
    """Test the create user view."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data."""
        cls.url = reverse('users:create')
        cls.redirect_url = reverse_lazy(SUCCESS_REDIRECT_PATH)
        cls.create_user_data = {
            'username': 'new_user',
            'password1': '1q2s3d4r',
            'password2': '1q2s3d4r',
        }

    def test_get_method_create_user(self) -> None:
        """Test the http status of render the create user form."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_method_create_user(self) -> None:
        """Test the http status and msg of submit the create form."""
        self.create_user_data['captcha_0'] = 'dummy-value'
        self.create_user_data['captcha_1'] = 'PASSED'
        response = self.client.post(self.url, self.create_user_data)
        self.assertRedirects(response, SUCCESS_REDIRECT_PATH, HTTPStatus.FOUND)
        flash_message_test(response, 'Пользователь создан')
        assert UserApp.objects.filter(username='new_user').exists()


class TestUpdateUserView(UserAuthTestCase):
    """Test the update user view."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data."""
        super().setUpTestData()
        cls.another_user = UserApp.objects.create(username='another_user')
        cls.url = reverse('users:update', kwargs={'pk': cls.user.id})
        cls.update_user_data = {
            'username': 'update_user',
            'password1': '1q2s3d4r',
            'password2': '1q2s3d4r',
        }

    def test_get_method_update_user_by_user(self) -> None:
        """Test update user by owner, the http status of form render."""
        response = self.get_auth_response(url=self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_method_update_user_by_user(self) -> None:
        """Test update user by owner, the http status of form submit."""
        self.update_user_data['captcha_0'] = 'dummy-value'
        self.update_user_data['captcha_1'] = 'PASSED'
        response = self.get_auth_response(
            path_schema=self.url,
            method='post',
            **self.update_user_data,
        )
        self.assertRedirects(response, SUCCESS_REDIRECT_PATH, HTTPStatus.FOUND)
        self.assertMessage(response, 'Пользователь обновлен')
        assert UserApp.objects.filter(username='update_user').exists()

    def test_post_method_update_user_by_another_user(self) -> None:
        """Test to permission denied to update user for another user."""
        response = self.get_auth_response(
            self.url,
            self.another_user,
            method='post',
            **self.update_user_data,
        )
        self.assertRedirects(response, NO_PERMISSION_URL, HTTPStatus.FOUND)
        self.assertMessage(response, NO_PERMISSION_MSG)
        assert not (UserApp.objects.filter(username='update_user').exists())

    def test_post_method_update_user_by_anonymous(self) -> None:
        """Test to permission denied to update user for anonymous."""
        response = self.client.post(self.url, self.update_user_data)
        self.assertRedirects(response, NO_PERMISSION_URL, HTTPStatus.FOUND)
        self.assertMessage(response, NO_PERMISSION_MSG)
        assert not UserApp.objects.filter(username='update_user').exists()


class TestDeleteUserView(UserAuthTestCase):
    """Test the delete user view."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data."""
        super().setUpTestData()
        cls.another_user = UserApp.objects.create(username='another_user')
        cls.url = reverse('users:delete', kwargs={'pk': cls.user.id})

    def test_get_method_delete_user_by_user(self) -> None:
        """Test delete user by owner, the http status of form render."""
        response = self.get_auth_response(path_schema=self.url)
        self.assertTrue(response.status_code, HTTPStatus.OK)

    def test_post_method_delete_user_by_user(self) -> None:
        """Test delete user by owner, the http status of form submit."""
        response = self.get_auth_response(path_schema=self.url, method='post')
        self.assertRedirects(response, SUCCESS_REDIRECT_PATH, HTTPStatus.FOUND)
        self.assertMessage(response, 'Пользователь удален')
        self.assertFalse(UserApp.objects.filter(pk=self.user.id).exists())

    def test_post_method_delete_user_by_another_user(self) -> None:
        """Tes delete user by another user."""
        response = self.get_auth_response(self.url, self.another_user)
        self.assertRedirects(response, NO_PERMISSION_URL, HTTPStatus.FOUND)
        self.assertMessage(response, NO_PERMISSION_MSG)
        self.assertTrue(UserApp.objects.filter(pk=self.user.id).exists())

    def test_post_method_delete_user_by_anonymous(self) -> None:
        """Test delete user by anonymous."""
        response = self.client.post(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, HTTPStatus.FOUND)
        self.assertMessage(response, NO_PERMISSION_MSG)
        self.assertTrue(UserApp.objects.filter(pk=self.user.id).exists())


class TestUserListView(UserAuthTestCase):
    """Test the user list view."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data."""
        super().setUpTestData()
        cls.admin = UserApp.objects.create_superuser(username='admin')
        cls.url = reverse('users:list')

    def test_show_user_list_to_admin(self) -> None:
        """Test display user list to admin, http status 200."""
        response = self.get_auth_response(
            user=self.admin,
            path_schema=self.url,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_show_user_list_to_user(self) -> None:
        """Test display user list to logged-in user, http status 302."""
        response = self.get_auth_response(user=self.user, path_schema=self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, HTTPStatus.FOUND)
        self.assertMessage(response, 'Нужны права администратора')

    def test_show_user_list_to_anonymous(self) -> None:
        """Test display user list to anonymous, http status 302."""
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, HTTPStatus.FOUND)
        self.assertMessage(response, 'Нужны права администратора')


class TestUserDetailView(UserAuthTestCase):
    """Test the user detail view."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data."""
        super().setUpTestData()
        cls.another_user = UserApp.objects.create(username='another_user')
        cls.url = reverse('users:detail', kwargs={'pk': cls.user.id})

    def test_show_user_detail_to_user(self) -> None:
        """Test show user detail to owner, http status 200."""
        response = self.get_auth_response(path_schema=self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_show_user_detail_to_another_user(self) -> None:
        """Test permission to display the detail for another user."""
        response = self.get_auth_response(self.url, self.another_user)
        self.assertRedirects(response, NO_PERMISSION_URL, HTTPStatus.FOUND)
        self.assertMessage(response, NO_PERMISSION_MSG)

    def test_show_user_detail_to_anonymous(self) -> None:
        """Test permission to display the detail for anonymous."""
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, HTTPStatus.FOUND)
        self.assertMessage(response, NO_PERMISSION_MSG)
