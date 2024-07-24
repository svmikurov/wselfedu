from django.test import Client, TestCase
from django.urls import reverse_lazy, reverse

from contrib.tests_extension import flash_message_test
from english.models import CategoryModel
from users.models import UserModel

CREATE_CATEGORY_PATH = 'english:categories_create'
DELETE_CATEGORY_PATH = 'english:categories_delete'
DETAIL_CATEGORY_PATH = 'english:categories_detail'
UPDATE_CATEGORY_PATH = 'english:categories_update'
CATEGORY_LIST_PATH = 'english:category_list'

NO_PERMISSION_MSG = 'Для доступа необходимо войти в приложение'
NO_PERMISSION_URL = reverse('users:login')

SUCCESS_CREATE_CATEGORY_MSG = 'Категория слов добавлена'
SUCCESS_UPDATE_CATEGORY_MSG = 'Категория слов изменена'
SUCCESS_DELETE_CATEGORY_MSG = 'Категория слов удалена'


class TestCreateCategoryView(TestCase):
    """Test create category view."""

    fixtures = ['tests/tests_english/fixtures/wse-fixtures-3.json']

    def setUp(self):
        """Set up data."""
        self.client: Client = Client()
        user_id = 3
        self.user = UserModel.objects.get(pk=user_id)
        self.create_data = {'name': 'new category'}
        self.url = reverse_lazy(CREATE_CATEGORY_PATH)

    def test_get_create_category_by_user(self):
        """Test create category by logged-in user, GET method page status 200.
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_create_category_by_user(self):
        """Test create category by logged-in user, POST method page status 302.
        """
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.create_data)

        self.assertRedirects(response, reverse(CATEGORY_LIST_PATH), 302)
        flash_message_test(response, SUCCESS_CREATE_CATEGORY_MSG)
        assert CategoryModel.objects.filter(name='new category').exists()

    def test_post_create_category_by_anonymous(self):
        """Test the permission denied to create a category for an anonymous."""
        response = self.client.post(self.url, self.create_data)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert not CategoryModel.objects.filter(name='new category').exists()


class TestUpdateCategoryView(TestCase):
    """Test update category view."""

    fixtures = ['tests/tests_english/fixtures/wse-fixtures-3.json']

    def setUp(self):
        """Set up data."""
        user_id = 3
        user_category_id = 1
        another_user_id = 4
        self.user = UserModel.objects.get(pk=user_id)
        self.another_user = UserModel.objects.get(pk=another_user_id)
        self.update_data = {'name': 'updated category'}
        self.url = reverse(
            UPDATE_CATEGORY_PATH, kwargs={'pk': user_category_id}
        )
        self.success_url = reverse_lazy(CATEGORY_LIST_PATH)

    def test_get_method_update_category_by_user(self):
        """Test update category by logged-in user, GET method page status 200.
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_method_update_category_by_user(self):
        """Test update category by logged-in user, POST method page status 302.
        """
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.update_data)
        self.assertRedirects(response, self.success_url, 302)
        flash_message_test(response, SUCCESS_UPDATE_CATEGORY_MSG)
        assert CategoryModel.objects.filter(name='updated category').exists()

    def test_post_method_update_category_by_another_user(self):
        """Test the permission denied to update a category for an another user.
        """
        self.client.force_login(self.another_user)
        response = self.client.post(self.url, self.update_data)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert not CategoryModel.objects.filter(name='updated category').exists()   # Noqa: E501

    def test_post_update_category_by_anonymous(self):
        """Test the permission denied to update a category for an anonymous.
        """
        response = self.client.post(self.url, self.update_data)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert not CategoryModel.objects.filter(name='updated category').exists()   # Noqa: E501


class TestDeleteCategoryView(TestCase):
    """Test delete category view."""

    fixtures = ['tests/tests_english/fixtures/wse-fixtures-3.json']

    def setUp(self):
        """Set up data."""
        user_id = 3
        self.user_category_id = 5
        self.user_protected_category_id = 1
        another_user_id = 4
        self.user = UserModel.objects.get(pk=user_id)
        self.another_user = UserModel.objects.get(pk=another_user_id)
        self.url = reverse(
            DELETE_CATEGORY_PATH,
            kwargs={'pk': self.user_category_id}
        )
        self.protected_url = reverse(
            DELETE_CATEGORY_PATH,
            kwargs={'pk': self.user_protected_category_id},
        )
        self.success_url = reverse(CATEGORY_LIST_PATH)
        self.protected_redirect = reverse(CATEGORY_LIST_PATH)

    def test_get_method_delete_category_by_user(self):
        """Test delete category by logged-in user, GET method page status 200.
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_method_delete_category_by_user(self):
        """Test delete category by logged-in user, POST method page status 302.
        """
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertRedirects(response, self.success_url, 302)
        flash_message_test(response, SUCCESS_DELETE_CATEGORY_MSG)
        assert not CategoryModel.objects.filter(
            pk=self.user_category_id
        ).exists()

    def test_post_method_delete_category_by_another_user(self):
        """Test the permission denied to delete a category for an another user.
        """
        self.client.force_login(self.another_user)
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert CategoryModel.objects.filter(pk=self.user_category_id).exists()

    def test_post_method_delete_category_by_anonymous(self):
        """Test the permission denied to delete a category for an anonymous."""
        response = self.client.post(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert CategoryModel.objects.filter(pk=self.user_category_id).exists()


class TestCategoryListView(TestCase):
    """Test category list view."""

    fixtures = ['tests/tests_english/fixtures/wse-fixtures-3.json']

    def setUp(self):
        """Set up data."""
        self.client = Client()
        self.user_id = 3
        self.user = UserModel.objects.get(pk=self.user_id)
        self.url = reverse(CATEGORY_LIST_PATH)

    def test_show_specific_category_list_to_specific_user(self):
        """
        Test display specific category list to specific user, page status 200.
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        # Assert page status 200.
        self.assertEqual(response.status_code, 200)

        # Assert by user id, that `category` contains only the user's
        # categories.
        sources = response.context["categories"]
        user_ids = set(sources.values_list('user', flat=True))
        self.assertTrue(*user_ids, self.user_id)

    def test_show_category_list_to_anonymous(self):
        """
        Test the permission denied to display a category list for an anonymous.
        """
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)


class TestCategoryDetailView(TestCase):
    """Test source detail view."""

    fixtures = ['tests/tests_english/fixtures/wse-fixtures-3.json']

    def setUp(self):
        """Set up data."""
        self.client: Client = Client()
        user_id = 3
        user_category_id = 1
        another_user_id = 4
        self.user = UserModel.objects.get(pk=user_id)
        self.another_user = UserModel.objects.get(pk=another_user_id)
        self.url = reverse(DETAIL_CATEGORY_PATH, kwargs={'pk': user_category_id})   # Noqa: E501

    def test_show_category_detail_to_user(self):
        """Test show category detail to user, page status 200."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_show_category_detail_to_another_user(self):
        """
        Test the permission denied to display a category detail for another
        user.
        """
        self.client.force_login(self.another_user)
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)

    def test_show_category_detail_to_anonymous(self):
        """
        Test the permission denied to display category details for anonymous.
        """
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
