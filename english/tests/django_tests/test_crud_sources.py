"""
Test CRUD sources.
"""
from django.test import TestCase
from django.urls import reverse_lazy

from contrib_app.contrib_test import flash_message_test
from english.models import SourceModel
from users.models import UserModel

SOURCES_LIST_PATH = 'english:sources_list'
"""Source list page path name.
"""


class TestListSources(TestCase):
    """Test list sources."""

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        """Preparing the testing environment."""
        self.admin = UserModel.objects.get(username='admin')
        self.user = UserModel.objects.get(username='user1')
        self.source_name1 = SourceModel.objects.get(pk=1).name
        self.source_name2 = SourceModel.objects.get(pk=2).name
        self.list_url = reverse_lazy(SOURCES_LIST_PATH)

        self.no_permissions_message = 'Вы пока не можете делать это'
        self.no_permissions_redirect = reverse_lazy('home')

    def test_get_list_by_admin(self):
        """Test source list page status 200 for admin."""
        self.client.force_login(self.admin)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_source_list_content(self):
        """Test source list page content."""
        self.client.force_login(self.admin)
        response = self.client.get(self.list_url)

        html = response.content.decode()
        self.assertInHTML(self.source_name1, html)
        self.assertInHTML(self.source_name2, html)

        # Does the sources list page contain "Изменить / Удалить"?
        self.assertIn('Изменить', html)
        self.assertIn('Удалить', html)

    def test_get_list_by_user(self):
        """Test source list page status 200 for auth user."""
        self.client.force_login(self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

        # Does the sources list page contain "Изменить / Удалить"?
        html = response.content.decode()
        self.assertNotIn('Изменить', html)
        self.assertNotIn('Удалить', html)

    def test_source_list_only_current_user(self):
        """Test show source list only of user."""
        self.client.force_login(self.user)
        response = self.client.get(self.list_url)
        object_list = response.context['object_list']

        self.assertTrue(len(object_list) == 2)
        self.assertTrue(object_list.contains(SourceModel.objects.get(id=5)))
        self.assertFalse(object_list.contains(SourceModel.objects.get(id=2)))

    def test_get_list_by_not_auth(self):
        """Test source list page status 200 for not auth user."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)


class TestCreateSource(TestCase):
    """Test create source."""

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        """Preparing the testing environment."""
        self.admin = UserModel.objects.get(username='admin')
        self.user = UserModel.objects.get(username='user1')
        self.new_source = {'name': 'new_source'}

        self.create_url = reverse_lazy('english:source_create')
        self.success_url = reverse_lazy(SOURCES_LIST_PATH)
        self.success_message = 'Источник слов добавлен'
        self.no_permissions_message = 'Вы пока не можете делать это'
        self.no_permissions_redirect = reverse_lazy('home')

    def test_get_create_by_admin(self):
        """Test get method page status 200, source creation by admin.
        """
        self.client.force_login(self.admin)
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)

    def test_post_create_by_admin(self):
        """Test post method page status 200, source creation by admin."""
        self.client.force_login(self.admin)
        response = self.client.post(self.create_url, self.new_source)
        self.assertRedirects(response, self.success_url, 302)
        flash_message_test(response, self.success_message)

        # Does the sources list page contain a new source?
        response = self.client.get(self.success_url)
        self.assertInHTML(self.new_source['name'], response.content.decode())

    def test_get_create_by_user(self):
        """Test get method page status 200, source creation by auth user."""
        self.client.force_login(self.user)
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)

    def test_post_create_by_user(self):
        """Test post method page status 200, source creation by auth user."""
        self.client.force_login(self.user)
        response = self.client.post(self.create_url, self.new_source)
        self.assertRedirects(response, self.success_url, 302)

    def test_create_source_by_user(self):
        """Test create source by user."""
        self.client.force_login(self.user)
        self.client.post(self.create_url, self.new_source)

        created_source = SourceModel.objects.filter(
            name=self.new_source['name'],
        )
        # Test add new source to DB.
        self.assertTrue(created_source.exists())
        # Test add user to source.
        self.assertTrue(created_source.values()[0]["user_id"] == self.user.id)

    def test_get_create_not_auth(self):
        """Get method by not auth user."""
        response = self.client.get(self.create_url)
        self.assertRedirects(response, self.no_permissions_redirect, 302)
        flash_message_test(response, self.no_permissions_message)

    def test_post_create_not_auth(self):
        """Post method by not auth user."""
        response = self.client.post(self.create_url, self.new_source)
        self.assertRedirects(response, self.no_permissions_redirect, 302)
        flash_message_test(response, self.no_permissions_message)


class TestUpdateSource(TestCase):
    """Test update source."""

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        """Preparing the testing environment."""
        self.admin = UserModel.objects.get(username='admin')
        self.user = UserModel.objects.get(username='user1')
        self.source = SourceModel.objects.get(pk=1)
        self.updated_source = {'name': 'updated_source'}

        self.update_url = reverse_lazy(
            'english:source_update', kwargs={'pk': 1}
        )
        self.success_url = reverse_lazy(SOURCES_LIST_PATH)
        self.success_message = 'Источник слов изменен'
        self.no_permissions_message = 'Вы пока не можете делать это'
        self.no_permissions_redirect = reverse_lazy('home')

    def test_get_update_by_admin(self):
        """Get method by admin."""
        self.client.force_login(self.admin)
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)

    def test_post_update_by_admin(self):
        """Post method by admin."""
        self.client.force_login(self.admin)
        response = self.client.post(self.update_url, self.updated_source)
        self.assertRedirects(response, self.success_url, 302)
        flash_message_test(response, self.success_message)

        # Does the sources list page contain an updated source?
        response = self.client.get(self.success_url)
        html = response.content.decode()
        self.assertInHTML(self.updated_source['name'], html)

    def test_get_update_by_user(self):
        """Get method by auth user."""
        self.client.force_login(self.user)
        response = self.client.get(self.update_url)
        self.assertRedirects(response, self.no_permissions_redirect, 302)
        flash_message_test(response, self.no_permissions_message)

    def test_post_update_by_user(self):
        """Post method by auth user."""
        self.client.force_login(self.user)
        response = self.client.post(self.update_url, self.updated_source)
        self.assertRedirects(response, self.no_permissions_redirect, 302)
        flash_message_test(response, self.no_permissions_message)

        # Does the db contain an updated_source?
        self.assertNotEqual(SourceModel.objects.filter(
            name=self.source
        ), self.updated_source['name'])

    def test_get_update_not_auth(self):
        """Get method by not auth user."""
        response = self.client.get(self.update_url)
        self.assertRedirects(response, self.no_permissions_redirect, 302)
        flash_message_test(response, self.no_permissions_message)

    def test_post_update_not_auth(self):
        """Post method by not auth user."""
        response = self.client.post(self.update_url, self.updated_source)
        self.assertRedirects(response, self.no_permissions_redirect, 302)
        flash_message_test(response, self.no_permissions_message)

        # Does the db contain a source name?
        self.assertTrue(SourceModel.objects.filter(
            name=self.source.name
        ).exists())


class TestDeleteSource(TestCase):
    """Test delete source."""

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        """Preparing the testing environment."""
        self.admin = UserModel.objects.get(username='admin')
        self.user = UserModel.objects.get(username='user1')

        # URL источника, которые не имеет связей.
        self.delete_url = reverse_lazy(
            'english:source_delete', kwargs={'pk': 1}
        )
        # URL источника, который имеет защищенные от удаления связи.
        self.delete_url_protected_source = reverse_lazy(
            'english:source_delete', kwargs={'pk': 2}
        )
        # Успешное удаление.
        self.success_url = reverse_lazy(SOURCES_LIST_PATH)
        self.success_message = 'Источник слов удален'
        # Удаление без прав на удаление.
        self.no_permissions_message = 'Вы пока не можете делать это'
        self.no_permissions_redirect = reverse_lazy('home')
        # Защита базы от удаления данных.
        self.protected_redirect = reverse_lazy(SOURCES_LIST_PATH)
        self.protected_message = (
            'Невозможно удалить этот объект, '
            'так как он используется в другом месте приложения'
        )

    def test_get_delete_by_admin(self):
        """Get method by admin."""
        self.client.force_login(self.admin)
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)

    def test_post_delete_by_admin(self):
        """Post method by admin."""
        self.client.force_login(self.admin)
        response = self.client.post(self.delete_url)
        self.assertRedirects(response, self.success_url, 302)
        flash_message_test(response, self.success_message)

        # Does the db contain a deleted source?
        self.assertFalse(SourceModel.objects.filter(pk=1).exists())

    def test_delete_protected_error(self):
        """Delete protected source."""
        self.client.force_login(self.admin)
        response = self.client.post(self.delete_url_protected_source)
        self.assertRedirects(response, self.protected_redirect, 302)
        flash_message_test(response, self.protected_message)

    def test_get_delete_by_user(self):
        """Get method by auth user."""
        self.client.force_login(self.user)
        response = self.client.get(self.delete_url)
        self.assertRedirects(response, self.no_permissions_redirect, 302)
        flash_message_test(response, self.no_permissions_message)

    def test_post_delete_by_user(self):
        """Post method by auth user."""
        self.client.force_login(self.user)
        response = self.client.post(self.delete_url)
        self.assertRedirects(response, self.no_permissions_redirect, 302)
        flash_message_test(response, self.no_permissions_message)

        # Does the db contain a source?
        self.assertTrue(SourceModel.objects.filter(pk=1).exists())

    def test_get_delete_not_auth(self):
        """Get method by not auth user."""
        response = self.client.get(self.delete_url)
        self.assertRedirects(response, self.no_permissions_redirect, 302)
        flash_message_test(response, self.no_permissions_message)

    def test_post_delete_not_auth(self):
        """Post method by not auth user."""
        response = self.client.post(self.delete_url)
        self.assertRedirects(response, self.no_permissions_redirect, 302)
        flash_message_test(response, self.no_permissions_message)

        # Does the db contain a source?
        self.assertTrue(SourceModel.objects.filter(pk=1).exists())
