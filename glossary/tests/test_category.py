"""Test CRUD category."""

from django.test import Client, TestCase
from django.urls import reverse

from contrib.tests.crud import (
    CreateTestMixin,
    DeleteTestMixin,
    ListTestMixin,
    UpdateTestMixin,
)
from glossary.models import GlossaryCategory
from users.models import UserApp


class CategoryTest(TestCase):
    """Glossary category tests data."""

    fixtures = ['users', 'glossary/tests/fixtures/category']

    def setUp(self) -> None:
        """Set up the test."""
        self.client = Client()

        # Items.
        self.item_pk = 1
        self.manager = GlossaryCategory.objects
        self.item = self.manager.get(pk=self.item_pk)
        self.item_data = {
            'name': 'category',
        }

        # Users.
        self.owner = UserApp.objects.get(pk=2)
        self.not_owner = UserApp.objects.get(pk=3)

        # Urls.
        self.url_create = reverse('glossary:category_create')
        self.url_list = reverse('glossary:category_list')
        self.url_update = reverse(
            'glossary:category_update', kwargs={'pk': self.item_pk}
        )
        self.url_delete = reverse(
            'glossary:category_delete', kwargs={'pk': self.item_pk}
        )

        # Redirect urls.
        self.url_create_redirect = self.url_list
        self.url_update_redirect = self.url_list
        self.url_delete_redirect = self.url_list
        self.url_not_owner_redirect = reverse('users:login')


class CreateTest(CreateTestMixin, CategoryTest):
    """Glossary category create tests."""


class ListTest(ListTestMixin, CategoryTest):
    """Glossary category list tests."""


class UpdateTest(UpdateTestMixin, CategoryTest):
    """Glossary category update tests."""


class DeleteTest(DeleteTestMixin, CategoryTest):
    """Glossary category delete tests."""
