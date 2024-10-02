"""Test foreign words pagination module."""

from django.test import Client, TestCase
from django.urls import reverse

from config.constants import CATEGORY, OBJECT_LIST
from foreign.models import Word, WordCategory
from users.models import UserApp

WORD_LIST_PATH = 'foreign:word_list'
PAGINATE_NUMBER = 20


class TestPagination(TestCase):
    """Test pagination."""

    fixtures = ['foreign/tests/fixtures/wse-fixtures-3.json']

    def setUp(self) -> None:
        """Set up data."""
        self.client: Client = Client()
        user_id = 3
        word_count = 50
        self.filtered_category_id = 2
        self.another_category_id = 3
        self.user = UserApp.objects.get(pk=user_id)
        self.url = reverse(WORD_LIST_PATH)

        # Add words fo filter and pagination
        for number in range(word_count):
            Word.objects.create(
                user=self.user,
                foreign_word=f'word_filtered_by_category_{number}',
                category=WordCategory.objects.get(
                    pk=self.filtered_category_id
                ),
            )
        for number in range(word_count):
            Word.objects.create(
                user=self.user,
                foreign_word=f'word_not_filtered_by_category_{number}',
                category=WordCategory.objects.get(pk=self.another_category_id),
            )

    def test_to_filter_paginated_page(self) -> None:
        """Test next page is also shown filtered by category words."""
        expected_category_variety = 1
        self.client.force_login(self.user)

        schema_query = f'?page=1&filtered_category={self.filtered_category_id}'
        page1_response = self.client.get(self.url + schema_query)
        object_list = page1_response.context[OBJECT_LIST]
        categories = set(object_list.values_list(CATEGORY, flat=True))

        assert len(object_list) == PAGINATE_NUMBER
        assert len(categories) == expected_category_variety
        assert self.filtered_category_id in categories

        schema_query = f'?page=2&filtered_category={self.filtered_category_id}'
        page2_response = self.client.get(self.url + schema_query)
        object_list = page2_response.context[OBJECT_LIST]
        categories = set(object_list.values_list(CATEGORY, flat=True))

        assert len(object_list) == PAGINATE_NUMBER
        assert len(categories) == expected_category_variety
        assert self.filtered_category_id in categories
