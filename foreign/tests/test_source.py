"""Test sources CRUD module."""

from django.test import Client, TestCase
from django.urls import reverse, reverse_lazy

from config.constants import (
    CREATE_SOURCE_PATH,
    DELETE_SOURCE_PATH,
    DETAIL_SOURCE_PATH,
    NAME,
    PK,
    SOURCE_LIST_PATH,
    SOURCES,
    UPDATE_SOURCE_PATH,
    USER,
)
from contrib.tests_extension import flash_message_test
from foreign.models import WordSource
from users.models import UserApp

NO_PERMISSION_MSG = 'Для доступа необходимо войти в приложение'
NO_PERMISSION_URL = reverse('users:login')

SUCCESS_CREATE_SOURCE_MSG = 'Источник слов добавлен'
SUCCESS_UPDATE_SOURCE_MSG = 'Источник слов изменен'
SUCCESS_DELETE_SOURCE_MSG = 'Источник слов удален'
PROTECT_DELETE_SOURCE_MSG = (
    'Невозможно удалить этот объект, так как он '
    'используется в другом месте приложения'
)


class TestCreateSourceView(TestCase):
    """Test create source view."""

    fixtures = ['tests/fixtures/foreign.json', 'tests/fixtures/users.json']

    def setUp(self) -> None:
        """Set up data."""
        self.client: Client = Client()
        user_id = 3
        self.user = UserApp.objects.get(pk=user_id)
        self.create_data = {NAME: 'new source'}
        self.url = reverse_lazy(CREATE_SOURCE_PATH)

    def test_get_method_create_source_by_user(self) -> None:
        """Test create source by logged-in user."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_method_create_source_by_user(self) -> None:
        """Test create source by logged-in user."""
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.create_data)

        self.assertRedirects(response, reverse(SOURCE_LIST_PATH), 302)
        flash_message_test(response, SUCCESS_CREATE_SOURCE_MSG)
        assert WordSource.objects.filter(name='new source').exists()

    def test_post_method_create_source_by_anonymous(self) -> None:
        """Test the permission to create source for an anonymous."""
        response = self.client.post(self.url, self.create_data)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert not WordSource.objects.filter(name='new source').exists()


class TestUpdateSourceView(TestCase):
    """Test update source view."""

    fixtures = ['tests/fixtures/foreign.json', 'tests/fixtures/users.json']

    def setUp(self) -> None:
        """Set up data."""
        user_id = 3
        user_source_id = 1
        another_user_id = 4
        self.user = UserApp.objects.get(pk=user_id)
        self.another_user = UserApp.objects.get(pk=another_user_id)
        self.update_data = {NAME: 'updated source'}
        self.url = reverse(UPDATE_SOURCE_PATH, kwargs={PK: user_source_id})
        self.success_url = reverse_lazy(SOURCE_LIST_PATH)

    def test_get_method_update_source_by_user(self) -> None:
        """Test update source by logged-in user."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_method_update_source_by_user(self) -> None:
        """Test update source by logged-in user."""
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.update_data)
        self.assertRedirects(response, self.success_url, 302)
        flash_message_test(response, SUCCESS_UPDATE_SOURCE_MSG)
        assert WordSource.objects.filter(name='updated source').exists()

    def test_post_method_update_source_by_another_user(self) -> None:
        """Test the permission to update source for an another user."""
        self.client.force_login(self.another_user)
        response = self.client.post(self.url, self.update_data)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert not WordSource.objects.filter(name='updated source').exists()

    def test_post_method_update_source_by_anonymous(self) -> None:
        """Test the permission to update source for an anonymous."""
        response = self.client.post(self.url, self.update_data)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert not WordSource.objects.filter(name='updated source').exists()


class TestDeleteSourceView(TestCase):
    """Test delete source view."""

    fixtures = ['tests/fixtures/foreign.json', 'tests/fixtures/users.json']

    def setUp(self) -> None:
        """Set up data."""
        user_id = 3
        self.user_source_id = 5
        self.user_protected_source_id = 1
        another_user_id = 4
        self.user = UserApp.objects.get(pk=user_id)
        self.another_user = UserApp.objects.get(pk=another_user_id)
        self.url = reverse(
            DELETE_SOURCE_PATH,
            kwargs={PK: self.user_source_id},
        )
        self.protected_url = reverse(
            DELETE_SOURCE_PATH,
            kwargs={PK: self.user_protected_source_id},
        )
        self.success_url = reverse(SOURCE_LIST_PATH)
        self.protected_redirect = reverse(SOURCE_LIST_PATH)

    def test_get_method_delete_source_by_user(self) -> None:
        """Test delete source by logged-in user."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_method_delete_source_by_user(self) -> None:
        """Test delete source by logged-in user."""
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertRedirects(response, self.success_url, 302)
        flash_message_test(response, SUCCESS_DELETE_SOURCE_MSG)
        assert not WordSource.objects.filter(pk=self.user_source_id).exists()

    def test_post_method_delete_source_by_another_user(self) -> None:
        """Test the permission to delete source for another user."""
        self.client.force_login(self.another_user)
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert WordSource.objects.filter(pk=self.user_source_id).exists()

    def test_post_method_delete_source_by_anonymous(self) -> None:
        """Test the permission to delete source for an anonymous."""
        response = self.client.post(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert WordSource.objects.filter(pk=self.user_source_id).exists()

    def test_delete_protected_source(self) -> None:
        """Test delete protected source."""
        self.client.force_login(self.user)
        response = self.client.post(self.protected_url)
        self.assertRedirects(response, self.protected_redirect, 302)
        flash_message_test(response, PROTECT_DELETE_SOURCE_MSG)
        assert WordSource.objects.filter(
            pk=self.user_protected_source_id
        ).exists()


class TestSourceListView(TestCase):
    """Test source list view."""

    fixtures = ['tests/fixtures/foreign.json', 'tests/fixtures/users.json']

    def setUp(self) -> None:
        """Set up data."""
        self.client: Client = Client()
        self.user_id = 3
        self.user = UserApp.objects.get(pk=self.user_id)
        self.url = reverse(SOURCE_LIST_PATH)

    def test_show_source_list_to_specific_user(self) -> None:
        """Test display specific source list to specific user."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        # Assert page status 200.
        self.assertEqual(response.status_code, 200)

        # Assert by user id, that `sources` contains
        # only the user's sources.
        sources = response.context[SOURCES]
        user_ids = set(sources.values_list(USER, flat=True))
        self.assertTrue(*user_ids, self.user_id)

    def test_show_source_list_to_anonymous(self) -> None:
        """Test display a source list for an anonymous."""
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)


class TestSourceDetailView(TestCase):
    """Test source detail view."""

    fixtures = ['tests/fixtures/foreign.json', 'tests/fixtures/users.json']

    def setUp(self) -> None:
        """Set up data."""
        self.client: Client = Client()
        user_id = 3
        user_source_id = 1
        another_user_id = 4
        self.user = UserApp.objects.get(pk=user_id)
        self.another_user = UserApp.objects.get(pk=another_user_id)
        self.url = reverse(DETAIL_SOURCE_PATH, kwargs={PK: user_source_id})

    def test_show_source_detail_to_user(self) -> None:
        """Test show source detail to user, page status 200."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_show_source_detail_to_another_user(self) -> None:
        """Test display a source detail for another user."""
        self.client.force_login(self.another_user)
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)

    def test_show_source_detail_to_anonymous(self) -> None:
        """Test display source details for an anonymous."""
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
