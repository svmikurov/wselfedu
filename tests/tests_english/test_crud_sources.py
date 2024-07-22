from django.test import Client, TestCase
from django.urls import reverse_lazy, reverse

from contrib.expanded_test import flash_message_test
from english.models import SourceModel
from users.models import UserModel

CREATE_SOURCE_PATH = 'english:source_create'
DELETE_SOURCE_PATH = 'english:source_delete'
DETAIL_SOURCE_PATH = 'english:source_detail'
UPDATE_SOURCE_PATH = 'english:source_update'
SOURCE_LIST_PATH = 'english:source_list'

NO_PERMISSION_MSG = 'Для доступа необходимо войти в приложение'
NO_PERMISSION_URL = reverse('users:login')

SUCCESS_CREATE_SOURCE_MSG = 'Источник слов добавлен'
SUCCESS_UPDATE_SOURCE_MSG = 'Источник слов изменен'
SUCCESS_DELETE_SOURCE_MSG = 'Источник слов удален'
PROTECT_DELETE_SOURCE_MSG = ('Невозможно удалить этот объект, так как он '
                             'используется в другом месте приложения')


class TestCreateSourceView(TestCase):
    """Test create source view."""

    fixtures = ['tests/tests_english/fixtures/wse-fixtures-3.json']

    def setUp(self):
        """Set up data."""
        self.client: Client = Client()
        user_id = 3
        self.user = UserModel.objects.get(pk=user_id)
        self.create_data = {'name': 'new source'}
        self.url = reverse_lazy(CREATE_SOURCE_PATH)

    def test_get_method_create_source_by_user(self):
        """Test create source by logged-in user, GET method page status 200."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_method_create_source_by_user(self):
        """Test create source by logged-in user, POST method page status 302.
        """
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.create_data)

        self.assertRedirects(response, reverse(SOURCE_LIST_PATH), 302)
        flash_message_test(response, SUCCESS_CREATE_SOURCE_MSG)
        assert SourceModel.objects.filter(name='new source').exists()

    def test_post_method_create_source_by_anonymous(self):
        """Test the permission denied to create source for an anonymous."""
        response = self.client.post(self.url, self.create_data)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert not SourceModel.objects.filter(name='new source').exists()


class TestUpdateSourceView(TestCase):
    """Test update source view."""

    fixtures = ['tests/tests_english/fixtures/wse-fixtures-3.json']

    def setUp(self):
        """Set up data."""
        user_id = 3
        user_source_id = 1
        another_user_id = 4
        self.user = UserModel.objects.get(pk=user_id)
        self.another_user = UserModel.objects.get(pk=another_user_id)
        self.update_data = {'name': 'updated source'}
        self.url = reverse(UPDATE_SOURCE_PATH, kwargs={'pk': user_source_id})
        self.success_url = reverse_lazy(SOURCE_LIST_PATH)

    def test_get_method_update_source_by_user(self):
        """Test update source by logged-in user, GET method page status 200."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_method_update_source_by_user(self):
        """Test update source by logged-in user, POST method page status 302.
        """
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.update_data)
        self.assertRedirects(response, self.success_url, 302)
        flash_message_test(response, SUCCESS_UPDATE_SOURCE_MSG)
        assert SourceModel.objects.filter(name='updated source').exists()

    def test_post_method_update_source_by_another_user(self):
        """Test the permission denied to update source for an another user."""
        self.client.force_login(self.another_user)
        response = self.client.post(self.url, self.update_data)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert not SourceModel.objects.filter(name='updated source').exists()

    def test_post_method_update_source_by_anonymous(self):
        """Test the permission denied to update source for an anonymous."""
        response = self.client.post(self.url, self.update_data)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert not SourceModel.objects.filter(name='updated source').exists()


class TestDeleteSourceView(TestCase):
    """Test delete source view."""

    fixtures = ['tests/tests_english/fixtures/wse-fixtures-3.json']

    def setUp(self):
        """Set up data."""
        user_id = 3
        self.user_source_id = 5
        self.user_protected_source_id = 1
        another_user_id = 4
        self.user = UserModel.objects.get(pk=user_id)
        self.another_user = UserModel.objects.get(pk=another_user_id)
        self.url = reverse(
            DELETE_SOURCE_PATH, kwargs={'pk': self.user_source_id},
        )
        self.protected_url = reverse(
            DELETE_SOURCE_PATH, kwargs={'pk': self.user_protected_source_id},
        )
        self.success_url = reverse(SOURCE_LIST_PATH)
        self.protected_redirect = reverse(SOURCE_LIST_PATH)

    def test_get_method_delete_source_by_user(self):
        """Test delete source by logged-in user, GET method page status 200."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_method_delete_source_by_user(self):
        """Test delete source by logged-in user, POST method page status 302.
        """
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertRedirects(response, self.success_url, 302)
        flash_message_test(response, SUCCESS_DELETE_SOURCE_MSG)
        assert not SourceModel.objects.filter(pk=self.user_source_id).exists()

    def test_post_method_delete_source_by_another_user(self):
        """Test the permission denied to delete source for another user."""
        self.client.force_login(self.another_user)
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert SourceModel.objects.filter(pk=self.user_source_id).exists()

    def test_post_method_delete_source_by_anonymous(self):
        """Test the permission denied to delete source for an anonymous."""
        response = self.client.post(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert SourceModel.objects.filter(pk=self.user_source_id).exists()

    def test_delete_protected_source(self):
        """Test delete protected source."""
        self.client.force_login(self.user)
        response = self.client.post(self.protected_url)
        self.assertRedirects(response, self.protected_redirect, 302)
        flash_message_test(response, PROTECT_DELETE_SOURCE_MSG)
        assert SourceModel.objects.filter(
            pk=self.user_protected_source_id
        ).exists()


class TestSourceListView(TestCase):
    """Test source list view."""

    fixtures = ['tests/tests_english/fixtures/wse-fixtures-3.json']

    def setUp(self):
        """Set up data."""
        self.client: Client = Client()
        self.user_id = 3
        self.user = UserModel.objects.get(pk=self.user_id)
        self.url = reverse(SOURCE_LIST_PATH)

    def test_show_source_list_to_specific_user(self):
        """Test display specific source list to specific user, page status 200.
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        # Assert page status 200.
        self.assertEqual(response.status_code, 200)

        # Assert by user id, that `sources` contains only the user's sources.
        sources = response.context["sources"]
        user_ids = set(sources.values_list('user', flat=True))
        self.assertTrue(*user_ids, self.user_id)

    def test_show_source_list_to_anonymous(self):
        """
        Test the permission denied to display a source list for an anonymous.
        """
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)


class TestSourceDetailView(TestCase):
    """Test source detail view."""

    fixtures = ['tests/tests_english/fixtures/wse-fixtures-3.json']

    def setUp(self):
        """Set up data."""
        self.client: Client = Client()
        user_id = 3
        user_source_id = 1
        another_user_id = 4
        self.user = UserModel.objects.get(pk=user_id)
        self.another_user = UserModel.objects.get(pk=another_user_id)
        self.url = reverse(DETAIL_SOURCE_PATH, kwargs={'pk': user_source_id})

    def test_show_source_detail_to_user(self):
        """Test show source detail to user, page status 200."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_show_source_detail_to_another_user(self):
        """
        Test the permission denied to display a source detail for another user.
        """
        self.client.force_login(self.another_user)
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)

    def test_show_source_detail_to_anonymous(self):
        """
        Test the permission denied to display source details for an anonymous.
        """
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
