"""Test CRUD category."""

from django.test import Client
from django.urls import reverse

from contrib.tests.crud import (
    CreateTest,
    DeleteTest,
    ListTest,
    TestData,
    UpdateTest,
)
from glossary.models import TermCategory
from users.models import UserApp


class CategoryTestData(TestData):
    """Term category tests data."""

    fixtures = ['users', 'glossary/tests/fixtures/category']

    def setUp(self) -> None:
        """Set up the test."""
        self.client = Client()

        # Items.
        self.item_pk = 1
        self.manager = TermCategory.objects
        self.item = self.manager.get(pk=self.item_pk)
        self.item_data = {
            'name': 'category',
        }

        # Users.
        self.owner_id = 2
        self.owner = UserApp.objects.get(pk=self.owner_id)
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


class CategoryCreateTest(CreateTest, CategoryTestData):
    """Term category create tests."""


class CategoryListTest(ListTest, CategoryTestData):
    """Term category list tests."""


class CategoryUpdateTest(UpdateTest, CategoryTestData):
    """Term category update tests."""


class CategoryDeleteTest(DeleteTest, CategoryTestData):
    """Term category delete tests."""
