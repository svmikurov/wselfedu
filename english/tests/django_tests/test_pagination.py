from django.test import Client, TestCase
from django.urls import reverse

from english.models import WordModel, CategoryModel
from users.models import UserModel

WORD_LIST_PATH = 'english:word_list'
PAGINATE_NUMBER = 20


class TestPagination(TestCase):
    """Test pagination."""

    fixtures = ['english/tests/fixtures/wse-fixtures-3.json']

    def setUp(self):
        """Set up data."""
        self.client: Client = Client()
        user_id = 3
        word_count = 50
        self.filtered_category_id = 2
        self.another_category_id = 3
        self.user = UserModel.objects.get(pk=user_id)
        self.url = reverse(WORD_LIST_PATH)

        # Add words fo filter and pagination
        for number in range(word_count):
            WordModel.objects.create(
                user=self.user,
                words_eng=f'word_filtered_by_category_{number}',
                category=CategoryModel.objects.get(pk=self.filtered_category_id),
            )
        for number in range(word_count):
            WordModel.objects.create(
                user=self.user,
                words_eng=f'word_not_filtered_by_category_{number}',
                category=CategoryModel.objects.get(pk=self.another_category_id),
            )

    def test_to_filter_paginated_page(self):
        """Test that the next page is also shown filtered by category words."""
        expected_category_variety = 1
        self.client.force_login(self.user)

        schema_query = f'?page=1&filtered_category={self.filtered_category_id}'
        page1_response = self.client.get(self.url + schema_query)
        object_list = page1_response.context["object_list"]
        categories = set(object_list.values_list('category', flat=True))

        assert len(object_list) == PAGINATE_NUMBER
        assert len(categories) == expected_category_variety
        assert self.filtered_category_id in categories

        schema_query = f'?page=2&filtered_category={self.filtered_category_id}'
        page2_response = self.client.get(self.url + schema_query)
        object_list = page2_response.context["object_list"]
        categories = set(object_list.values_list('category', flat=True))

        assert len(object_list) == PAGINATE_NUMBER
        assert len(categories) == expected_category_variety
        assert self.filtered_category_id in categories
