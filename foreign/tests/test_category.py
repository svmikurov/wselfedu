"""Tes categories CRUD module."""

from django.test import Client, TestCase
from django.urls import reverse, reverse_lazy

from config.constants import (
    CATEGORIES,
    CATEGORY_LIST_PATH,
    CREATE_CATEGORY_PATH,
    DELETE_CATEGORY_PATH,
    DETAIL_CATEGORY_PATH,
    NAME,
    PK,
    UPDATE_CATEGORY_PATH,
    USER,
)
from contrib.tests_extension import flash_message_test
from foreign.models import WordCategory
from users.models import UserApp

NO_PERMISSION_MSG = 'Для доступа необходимо войти в приложение'
NO_PERMISSION_URL = reverse('users:login')

SUCCESS_CREATE_CATEGORY_MSG = 'Категория слов добавлена'
SUCCESS_UPDATE_CATEGORY_MSG = 'Категория слов изменена'
SUCCESS_DELETE_CATEGORY_MSG = 'Категория слов удалена'


class TestCreateCategoryView(TestCase):
    """Test create category view."""

    fixtures = ['foreign/tests/fixtures/wse-fixtures-3.json']

    def setUp(self) -> None:
        """Set up data."""
        self.client: Client = Client()
        user_id = 3
        self.user = UserApp.objects.get(pk=user_id)
        self.create_data = {NAME: 'new category'}
        self.url = reverse_lazy(CREATE_CATEGORY_PATH)

    def test_get_create_category_by_user(self) -> None:
        """Test create category by logged-in user200."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_create_category_by_user(self) -> None:
        """Test create category by logged-in user."""
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.create_data)

        self.assertRedirects(response, reverse(CATEGORY_LIST_PATH), 302)
        flash_message_test(response, SUCCESS_CREATE_CATEGORY_MSG)
        assert WordCategory.objects.filter(name='new category').exists()

    def test_post_create_category_by_anonymous(self) -> None:
        """Test the permission to create a category for an anonymous."""
        response = self.client.post(self.url, self.create_data)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert not WordCategory.objects.filter(name='new category').exists()


class TestUpdateCategoryView(TestCase):
    """Test update category view."""

    fixtures = ['foreign/tests/fixtures/wse-fixtures-3.json']

    def setUp(self) -> None:
        """Set up data."""
        user_id = 3
        user_category_id = 1
        another_user_id = 4
        self.user = UserApp.objects.get(pk=user_id)
        self.another_user = UserApp.objects.get(pk=another_user_id)
        self.update_data = {NAME: 'updated category'}
        self.url = reverse(UPDATE_CATEGORY_PATH, kwargs={PK: user_category_id})
        self.success_url = reverse_lazy(CATEGORY_LIST_PATH)

    def test_get_method_update_category_by_user(self) -> None:
        """Test update category by logged-in user."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_method_update_category_by_user(self) -> None:
        """Test update category by logged-in user."""
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.update_data)
        self.assertRedirects(response, self.success_url, 302)
        flash_message_test(response, SUCCESS_UPDATE_CATEGORY_MSG)
        assert WordCategory.objects.filter(name='updated category').exists()

    def test_post_method_update_category_by_another_user(self) -> None:
        """Test permission to update a category for an another user."""
        self.client.force_login(self.another_user)
        response = self.client.post(self.url, self.update_data)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert not WordCategory.objects.filter(
            name='updated category'
        ).exists()  # Noqa: E501

    def test_post_update_category_by_anonymous(self) -> None:
        """Test the permission to update a category for an anonymous."""
        response = self.client.post(self.url, self.update_data)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert not WordCategory.objects.filter(
            name='updated category'
        ).exists()  # Noqa: E501


class TestDeleteCategoryView(TestCase):
    """Test delete category view."""

    fixtures = ['foreign/tests/fixtures/wse-fixtures-3.json']

    def setUp(self) -> None:
        """Set up data."""
        user_id = 3
        self.user_category_id = 5
        self.user_protected_category_id = 1
        another_user_id = 4
        self.user = UserApp.objects.get(pk=user_id)
        self.another_user = UserApp.objects.get(pk=another_user_id)
        self.url = reverse(
            DELETE_CATEGORY_PATH, kwargs={PK: self.user_category_id}
        )
        self.protected_url = reverse(
            DELETE_CATEGORY_PATH,
            kwargs={PK: self.user_protected_category_id},
        )
        self.success_url = reverse(CATEGORY_LIST_PATH)
        self.protected_redirect = reverse(CATEGORY_LIST_PATH)

    def test_get_method_delete_category_by_user(self) -> None:
        """Test delete category by logged-in user."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_method_delete_category_by_user(self) -> None:
        """Test delete category by logged-in user."""
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertRedirects(response, self.success_url, 302)
        flash_message_test(response, SUCCESS_DELETE_CATEGORY_MSG)
        assert not WordCategory.objects.filter(
            pk=self.user_category_id
        ).exists()

    def test_post_method_delete_category_by_another_user(self) -> None:
        """Test delete a category for an another user."""
        self.client.force_login(self.another_user)
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert WordCategory.objects.filter(pk=self.user_category_id).exists()

    def test_post_method_delete_category_by_anonymous(self) -> None:
        """Test the permission to delete a category for an anonymous."""
        response = self.client.post(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert WordCategory.objects.filter(pk=self.user_category_id).exists()


class TestCategoryListView(TestCase):
    """Test category list view."""

    fixtures = ['foreign/tests/fixtures/wse-fixtures-3.json']

    def setUp(self) -> None:
        """Set up data."""
        self.client = Client()
        self.user_id = 3
        self.user = UserApp.objects.get(pk=self.user_id)
        self.url = reverse(CATEGORY_LIST_PATH)

    def test_show_specific_category_list_to_specific_user(self) -> None:
        """Test display specific category list to specific user."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        # Assert page status 200.
        self.assertEqual(response.status_code, 200)

        # Assert by user id, that `category` contains only the user's
        # categories.
        sources = response.context[CATEGORIES]
        user_ids = set(sources.values_list(USER, flat=True))
        self.assertTrue(*user_ids, self.user_id)

    def test_show_category_list_to_anonymous(self) -> None:
        """Test to display a category list for an anonymous."""
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)


class TestCategoryDetailView(TestCase):
    """Test source detail view."""

    fixtures = ['foreign/tests/fixtures/wse-fixtures-3.json']

    def setUp(self) -> None:
        """Set up data."""
        self.client: Client = Client()
        user_id = 3
        user_category_id = 1
        another_user_id = 4
        self.user = UserApp.objects.get(pk=user_id)
        self.another_user = UserApp.objects.get(pk=another_user_id)
        self.url = reverse(DETAIL_CATEGORY_PATH, kwargs={PK: user_category_id})

    def test_show_category_detail_to_user(self) -> None:
        """Test show category detail to user, page status 200."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_show_category_detail_to_another_user(self) -> None:
        """Test display a category detail for another."""
        self.client.force_login(self.another_user)
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)

    def test_show_category_detail_to_anonymous(self) -> None:
        """Test display category details for anonymous."""
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
