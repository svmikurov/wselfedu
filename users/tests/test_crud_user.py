from django.test import Client, TestCase
from django.urls import reverse_lazy, reverse

from contrib_app.contrib_test import flash_message_test
from users.models import UserModel

CREATE_USER_PATH = 'users:create'
DELETE_USER_PATH = 'users:delete'
DETAIL_USER_PATH = 'users:detail'
UPDATE_USER_PATH = 'users:update'
USER_LIST_PATH = 'users:list'
LOGIN_PATH = 'users:login'

NO_PERMISSION_MSG = 'Для доступа необходимо войти в приложение'
NO_ADMIN_PERMISSION_MSG = 'Нужны права администратора'
NO_PERMISSION_URL = reverse(LOGIN_PATH)

SUCCESS_CREATE_USER_MSG = 'Пользователь создан'
SUCCESS_UPDATE_USER_MSG = 'Пользователь обновлен'
SUCCESS_DELETE_USER_MSG = 'Пользователь удален'
SUCCESS_REDIRECT_PATH = '/users/login/'

PROTECT_REDIRECT_URL = 'home'
PROTECT_DELETE_MSG = ('Невозможно удалить этот объект, так как он '
                      'используется в другом месте приложения')


class TestCreateUserView(TestCase):
    """Test create user view."""

    fixtures = ['english/tests/fixtures/wse-fixtures-3.json']

    def setUp(self):
        """Set up data."""
        self.client: Client = Client()
        self.url = reverse(CREATE_USER_PATH)
        self.redirect_url = reverse_lazy(SUCCESS_REDIRECT_PATH)
        self.create_data = {
            'username': 'new_user',
            'password1': '1q2s3d4r',
            'password2': '1q2s3d4r',
        }

    def test_get_method_create_user(self):
        """Test create user, GET method page status 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_method_create_user(self):
        """Test create user, POST method page status 302."""
        response = self.client.post(self.url, self.create_data)
        self.assertRedirects(response, SUCCESS_REDIRECT_PATH, 302)
        flash_message_test(response, SUCCESS_CREATE_USER_MSG)
        assert (UserModel.objects.filter(username='new_user').exists())


class TestUpdateUserView(TestCase):
    """Test update user view."""

    fixtures = ['english/tests/fixtures/wse-fixtures-3.json']

    def setUp(self):
        """Set up data."""
        self.client: Client = Client()
        user_id = 3
        another_user_id = 4
        self.user = UserModel.objects.get(pk=user_id)
        self.another_user = UserModel.objects.get(pk=another_user_id)
        self.url = reverse(UPDATE_USER_PATH, kwargs={'pk': user_id})
        self.update_data = {
            'username': 'update_user',
            'password1': '1q2s3d4r',
            'password2': '1q2s3d4r',
        }

    def test_get_method_update_user_by_user(self):
        """Test update user by user, GET method page status 200."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_method_update_user_by_user(self):
        """Test update user by user, POST method page status 302."""
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.update_data)

        self.assertRedirects(response, SUCCESS_REDIRECT_PATH, 302)
        flash_message_test(response, SUCCESS_UPDATE_USER_MSG)
        assert UserModel.objects.filter(username='update_user').exists()

    def test_post_method_update_user_by_another_user(self):
        """Test to permission denied update user for another user."""
        self.client.force_login(self.another_user)
        response = self.client.post(self.url, self.update_data)

        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert not UserModel.objects.filter(username='update_user').exists()

    def test_post_method_update_user_by_anonymous(self):
        """Test to permission denied update user for anonymous."""
        response = self.client.post(self.url, self.update_data)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert not UserModel.objects.filter(username='update_user').exists()


class TestDeleteUserView(TestCase):
    """Test delete user view."""

    fixtures = ['english/tests/fixtures/wse-fixtures-3.json']

    def setUp(self):
        """Set up data."""
        self.client: Client = Client()
        self.user_id = 4
        self.protected_delete_user_id = 3
        another_user_id = 3
        self.user = UserModel.objects.get(pk=self.user_id)
        self.another_user = UserModel.objects.get(pk=another_user_id)
        self.protected_delete_user = UserModel.objects.get(
            pk=self.protected_delete_user_id
        )
        self.url = reverse(DELETE_USER_PATH, kwargs={'pk': self.user_id})
        self.delete_protected_url = reverse(
            DELETE_USER_PATH, kwargs={'pk': self.protected_delete_user_id}
        )

    def test_get_method_delete_user_by_user(self):
        """Test delete user by user, GET method page status 200."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertTrue(response.status_code, 200)

    def test_post_method_delete_user_by_user(self):
        """Test delete user by user, POST method page status 302."""
        self.client.force_login(self.user)
        response = self.client.post(self.url)

        self.assertRedirects(response, SUCCESS_REDIRECT_PATH, 302)
        flash_message_test(response, SUCCESS_DELETE_USER_MSG)
        assert not UserModel.objects.filter(pk=self.user_id)

    def test_post_method_delete_user_by_another_user(self):
        """Tes delete user by another user, POST method page status 302."""
        self.client.force_login(self.another_user)
        response = self.client.get(self.url)

        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert UserModel.objects.filter(pk=self.user_id).exists()

    def test_post_method_delete_user_by_anonymous(self):
        """Test delete user by anonymous, POST method page status 302."""
        response = self.client.post(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert UserModel.objects.filter(pk=self.user_id).exists()

    def test_delete_protected_user(self):
        """Test delete protected user."""
        self.client.force_login(self.protected_delete_user)
        response = self.client.post(self.delete_protected_url)
        self.assertRedirects(response, reverse(PROTECT_REDIRECT_URL), 302)
        flash_message_test(response, PROTECT_DELETE_MSG)
        assert UserModel.objects.filter(
            pk=self.protected_delete_user_id
        ).exists()


class TestUserListView(TestCase):
    """Test list user view."""

    fixtures = ['english/tests/fixtures/wse-fixtures-3.json']

    def setUp(self):
        """Set up data."""
        self.clint: Client = Client()
        admin_id = 1
        user_id = 3
        self.admin = UserModel.objects.get(pk=admin_id)
        self.user = UserModel.objects.get(pk=user_id)
        self.url = reverse(USER_LIST_PATH)

    def test_show_user_list_to_admin(self):
        """Test display user list to admin, page status 200."""
        self.clint.force_login(self.admin)
        response = self.client.get(self.url)
        self.assertTrue(response.status_code, 200)

    def test_show_user_list_to_user(self):
        """Test display user list to logged-in user, page status 302."""
        self.clint.force_login(self.user)
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_ADMIN_PERMISSION_MSG)

    def test_show_user_list_to_anonymous(self):
        """Test display user list to anonymous, page status 302."""
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_ADMIN_PERMISSION_MSG)


class TestUserDetailView(TestCase):
    """Test user detail view."""

    fixtures = ['english/tests/fixtures/wse-fixtures-3.json']

    def setUp(self):
        """Set up data."""
        self.client: Client = Client()
        user_id = 3
        another_user_id = 4
        self.user = UserModel.objects.get(pk=user_id)
        self.another_user = UserModel.objects.get(pk=another_user_id)
        self.url = reverse(DETAIL_USER_PATH, kwargs={'pk': user_id})

    def test_show_user_detail_to_user(self):
        """Test show user detail to user, page status 200."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_show_user_detail_to_another_user(self):
        """Test permission denied to display a user detail for another user."""
        self.client.force_login(self.another_user)
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)

    def test_show_user_detail_to_anonymous(self):
        """Test permission denied to display user details for anonymous user.
        """
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
