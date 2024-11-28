"""Tests of serializer."""

from rest_framework.test import APITestCase

from foreign.models import WordCategory
from foreign.serializers import WordCategorySerializer
from users.models import UserApp


class TestWordCategorySerializer(APITestCase):
    """Test the WordCategorySerializer."""

    fixtures = ['users', 'word_category']

    def setUp(self) -> None:
        """Set up."""
        self.user_pk = 3
        self.user = UserApp.objects.get(pk=self.user_pk)
        self.attributes = {'user': self.user, 'name': 'book'}
        self.category = WordCategory.objects.create(**self.attributes)

        self.fields = ['id', 'name']
        self.serializer = WordCategorySerializer(instance=self.category)
        # self.serializer = WordCategorySerializer(
        #     self.categories, many=True,
        # )

        self.data = self.serializer.data

    def test_contains_expected_fields(self) -> None:
        """Test that contain expected fields."""
        self.assertEqual(set(self.data.keys()), set(self.fields))

    def test_fields_content(self) -> None:
        """Test a fields contents."""
        self.assertEqual(self.data['name'], self.attributes['name'])
