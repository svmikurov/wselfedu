"""
Test CRUD categories.
For now:
    - can reade categories: admin, auth user;
    - can create, update and delete category: admin.

Fixtures are created and taken from the db-wse-fixtures.sqlite3 and contain:
    - users: admin, user1;
"""

from django.test import TestCase
from django.urls import reverse_lazy

from contrib_app.contrib_test import flash_message_test
from users.models import UserModel


class TestListCategories(TestCase):
    """Test list categories."""

    fixtures = ['english/tests/fixtures/fixtures.json']

    def setUp(self):
        """Preparing the testing environment."""
        self.admin = UserModel.objects.get(username='admin')
        self.user = UserModel.objects.get(username='user1')
        self.create_url = reverse_lazy('eng:categories_list')

        self.no_permissions_message = 'Вы пока не можете делать это'
        self.no_permissions_redirect = reverse_lazy('home')

    def test_get_list_by_admin(self):
        """Get method by admin."""
        self.client.force_login(self.admin)
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)

    def test_get_list_by_user(self):
        """Get method by auth user."""
        self.client.force_login(self.user)
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)

    def test_get_list_by_not_auth(self):
        """Get method by not auth user."""
        response = self.client.get(self.create_url)
        self.assertRedirects(response, self.no_permissions_redirect, 302)
        flash_message_test(response, self.no_permissions_message)


class TestCreateCategories(TestCase):
    """Test create category."""

    fixtures = ['english/tests/fixtures/fixtures.json']

    def setUp(self):
        """Preparing the testing environment."""
        self.admin = UserModel.objects.get(username='admin')
        self.user = UserModel.objects.get(username='user1')
        self.new_category = {'name': 'new_category'}

        self.create_url = reverse_lazy('eng:categories_create')
        self.success_url = reverse_lazy('eng:categories_list')
        self.success_message = 'Категория добавлена'
        self.no_permissions_message = 'Вы пока не можете делать это'
        self.no_permissions_redirect = reverse_lazy('home')

    #################################
    # Test create with permissions. #
    #################################
    def test_get_create_by_admin(self):
        """Get method by admin."""
        self.client.force_login(self.admin)
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)

    def test_post_create_by_admin(self):
        """Post method by admin."""
        self.client.force_login(self.admin)
        response = self.client.post(self.create_url, self.new_category)
        self.assertRedirects(response, self.success_url, 302)
        flash_message_test(response, self.success_message)

        # Contains a list of categories, a new category.
        response = self.client.get(self.success_url)
        self.assertInHTML(self.new_category['name'], response.content.decode())

    ####################################
    # Test create with no permissions. #
    ####################################
    def test_get_create_by_user(self):
        """Get method by auth user."""
        self.client.force_login(self.user)
        response = self.client.get(self.create_url)
        self.assertRedirects(response, self.no_permissions_redirect, 302)
        flash_message_test(response, self.no_permissions_message)

    def test_post_create_by_user(self):
        """Post method by auth user."""
        self.client.force_login(self.user)
        response = self.client.post(self.create_url, self.new_category)
        self.assertRedirects(response, self.no_permissions_redirect, 302)
        flash_message_test(response, self.no_permissions_message)

    def test_get_create_not_auth(self):
        """Get method by not auth user."""
        response = self.client.get(self.create_url)
        self.assertRedirects(response, self.no_permissions_redirect, 302)
        flash_message_test(response, self.no_permissions_message)

    def test_post_create_not_auth(self):
        """Post method by not auth user."""
        response = self.client.post(self.create_url, self.new_category)
        self.assertRedirects(response, self.no_permissions_redirect, 302)
        flash_message_test(response, self.no_permissions_message)
