"""Test CRUD term."""

from django.test import Client
from django.urls import reverse

from contrib.tests.crud import (
    CreateTest,
    DeleteTest,
    DetailTest,
    ListTest,
    TestData,
    UpdateTest,
)
from glossary.models import Glossary
from users.models import UserApp


class TermTestData(TestData):
    """Glossary term tests data."""

    fixtures = ['users', 'terms']

    def setUp(self) -> None:
        """Set up the test."""
        self.client = Client()

        # Items.
        self.item_pk = 1
        self.manager = Glossary.objects
        self.item = self.manager.get(pk=self.item_pk)
        self.item_data = {
            'term': 'term',
        }

        # Users.
        self.owner_id = 2
        self.owner = UserApp.objects.get(pk=self.owner_id)
        self.not_owner = UserApp.objects.get(pk=3)

        # Urls.
        self.url_create = reverse('glossary:term_create')
        self.url_list = reverse('glossary:term_list')
        self.url_update = reverse(
            'glossary:term_update', kwargs={'pk': self.item_pk}
        )
        self.url_detail = reverse(
            'glossary:term_detail', kwargs={'pk': self.item_pk}
        )
        self.url_delete = reverse(
            'glossary:term_delete', kwargs={'pk': self.item_pk}
        )

        # Redirect urls.
        self.url_create_redirect = self.url_list
        self.url_update_redirect = self.url_list
        self.url_delete_redirect = self.url_list
        self.url_not_owner_redirect = reverse('users:login')


class TermCreateTest(CreateTest, TermTestData):
    """Glossary term create tests."""


class TermListTest(ListTest, TermTestData):
    """Glossary term list tests."""


class TermUpdateTest(UpdateTest, TermTestData):
    """Glossary term update tests."""


class TermDetailTest(DetailTest, TermTestData):
    """Glossary term detail tests."""


class TermDeleteTest(DeleteTest, TermTestData):
    """Glossary term delete tests."""
