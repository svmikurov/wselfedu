from django.test import TestCase
from django.urls import reverse, reverse_lazy

from contrib.tests_extension import UserAuthTestCase, flash_message_test
from users.models import UserModel

NO_PERMISSION_MSG = 'Для доступа необходимо войти в приложение'
NO_PERMISSION_URL = reverse('users:login')
SUCCESS_REDIRECT_PATH = '/users/login/'


class TestCreateUserView(TestCase):
    """Create user view test."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        cls.url = reverse('users:create')
        cls.redirect_url = reverse_lazy(SUCCESS_REDIRECT_PATH)
        cls.create_user_data = {
            'username': 'new_user',
            'password1': '1q2s3d4r',
            'password2': '1q2s3d4r',
        }

    def test_get_method_create_user(self):
        """Test create user, GET method success status."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_method_create_user(self):
        """Test create user, POST method redirect status."""
        response = self.client.post(self.url, self.create_user_data)
        self.assertRedirects(response, SUCCESS_REDIRECT_PATH, 302)
        flash_message_test(response, 'Пользователь создан')
        assert UserModel.objects.filter(username='new_user').exists()


class TestUpdateUserView(UserAuthTestCase):
    """Update user view test."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        super().setUpTestData()
        cls.another_user = UserModel.objects.create(username='another_user')
        cls.url = reverse('users:update', kwargs={'pk': cls.user.id})
        cls.update_user_data = {
            'username': 'update_user',
            'password1': '1q2s3d4r',
            'password2': '1q2s3d4r',
        }

    def test_get_method_update_user_by_user(self):
        """Test update user by user, GET method success status."""
        response = self.get_auth_response(url=self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_method_update_user_by_user(self):
        """Test update user by user, POST method page status 302."""
        response = self.get_auth_response(
            path_schema=self.url,
            method='post',
            **self.update_user_data,
        )
        self.assertRedirects(response, SUCCESS_REDIRECT_PATH, 302)
        self.assertMessage(response, 'Пользователь обновлен')
        assert UserModel.objects.filter(username='update_user').exists()

    def test_post_method_update_user_by_another_user(self):
        """Test to permission denied update user for another user."""
        response = self.get_auth_response(
            self.url,
            self.another_user,
            method='post',
            **self.update_user_data,
        )
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        self.assertMessage(response, NO_PERMISSION_MSG)
        assert not (UserModel.objects.filter(username='update_user').exists())

    def test_post_method_update_user_by_anonymous(self):
        """Test to permission denied update user for anonymous."""
        response = self.client.post(self.url, self.update_user_data)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        self.assertMessage(response, NO_PERMISSION_MSG)
        assert not UserModel.objects.filter(username='update_user').exists()


class TestDeleteUserView(UserAuthTestCase):
    """Delete user view test."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        super().setUpTestData()
        cls.another_user = UserModel.objects.create(username='another_user')
        cls.url = reverse('users:delete', kwargs={'pk': cls.user.id})

    def test_get_method_delete_user_by_user(self):
        """Test delete user by user, GET method page status 200."""
        response = self.get_auth_response(path_schema=self.url)
        self.assertTrue(response.status_code, 200)

    def test_post_method_delete_user_by_user(self):
        """Test delete user by user, POST method page status 302."""
        response = self.get_auth_response(path_schema=self.url, method='post')
        self.assertRedirects(response, SUCCESS_REDIRECT_PATH, 302)
        self.assertMessage(response, 'Пользователь удален')
        self.assertFalse(UserModel.objects.filter(pk=self.user.id).exists())

    def test_post_method_delete_user_by_another_user(self):
        """Tes delete user by another user."""
        response = self.get_auth_response(self.url, self.another_user)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        self.assertMessage(response, NO_PERMISSION_MSG)
        self.assertTrue(UserModel.objects.filter(pk=self.user.id).exists())

    def test_post_method_delete_user_by_anonymous(self):
        """Test delete user by anonymous."""
        response = self.client.post(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        self.assertMessage(response, NO_PERMISSION_MSG)
        self.assertTrue(UserModel.objects.filter(pk=self.user.id).exists())


class TestUserListView(UserAuthTestCase):
    """List user view test."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        super().setUpTestData()
        cls.admin = UserModel.objects.create_superuser(username='admin')
        cls.url = reverse('users:list')

    def test_show_user_list_to_admin(self):
        """Test display user list to admin, page status 200."""
        response = self.get_auth_response(
            user=self.admin,
            path_schema=self.url,
        )
        self.assertEqual(response.status_code, 200)

    def test_show_user_list_to_user(self):
        """Test display user list to logged-in user, page status 302."""
        response = self.get_auth_response(user=self.user, path_schema=self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        self.assertMessage(response, 'Нужны права администратора')

    def test_show_user_list_to_anonymous(self):
        """Test display user list to anonymous, page status 302."""
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        self.assertMessage(response, 'Нужны права администратора')


class TestUserDetailView(UserAuthTestCase):
    """User detail view test."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        super().setUpTestData()
        cls.another_user = UserModel.objects.create(username='another_user')
        cls.url = reverse('users:detail', kwargs={'pk': cls.user.id})

    def test_show_user_detail_to_user(self):
        """Test show user detail to user, page status 200."""
        response = self.get_auth_response(path_schema=self.url)
        self.assertEqual(response.status_code, 200)

    def test_show_user_detail_to_another_user(self):
        """Test permission to display for another user."""
        response = self.get_auth_response(self.url, self.another_user)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        self.assertMessage(response, NO_PERMISSION_MSG)

    def test_show_user_detail_to_anonymous(self):
        """Test permission to display for anonymous user."""
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        self.assertMessage(response, NO_PERMISSION_MSG)
