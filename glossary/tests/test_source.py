"""Test CRUD source."""

from django.test import Client, TestCase
from django.urls import reverse

from contrib.tests.crud import (
    CreateTestMixin,
    DeleteTestMixin,
    ListTestMixin,
    UpdateTestMixin,
)
from glossary.models import TermSource
from users.models import UserApp


class SourceTest(TestCase):
    """Glossary Source tests data."""

    fixtures = ['users', 'glossary/tests/fixtures/source']

    def setUp(self) -> None:
        """Set up the test."""
        self.client = Client()

        # Items.
        self.item_pk = 1
        self.manager = TermSource.objects
        self.item = self.manager.get(pk=self.item_pk)
        self.item_data = {
            'name': 'source',
        }

        # Users.
        self.owner = UserApp.objects.get(pk=2)
        self.not_owner = UserApp.objects.get(pk=3)

        # Urls.
        self.url_create = reverse('glossary:source_create')
        self.url_list = reverse('glossary:source_list')
        self.url_update = reverse(
            'glossary:source_update', kwargs={'pk': self.item_pk}
        )
        self.url_delete = reverse(
            'glossary:source_delete', kwargs={'pk': self.item_pk}
        )

        # Redirect urls.
        self.url_create_redirect = self.url_list
        self.url_update_redirect = self.url_list
        self.url_delete_redirect = self.url_list
        self.url_not_owner_redirect = reverse('users:login')


class CreateTest(CreateTestMixin, SourceTest):
    """Glossary source create tests."""


class ListTest(ListTestMixin, SourceTest):
    """Glossary source list tests."""


class UpdateTest(UpdateTestMixin, SourceTest):
    """Glossary source update tests."""


class DeleteTest(DeleteTestMixin, SourceTest):
    """Glossary source delete tests."""
