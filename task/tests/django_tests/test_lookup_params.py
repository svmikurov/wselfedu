from django.test import TestCase

from english.models import WordModel
from task.services import LookupParams


class TestLookupParams(TestCase):
    """Test get Word Queryset by user parameters."""

    fixtures = ['task/tests/fixtures/wse-fixtures-4.json']

    @classmethod
    def setUpTestData(cls):
        """Set up database data."""
        pass

    def test_lookup_by_user_id(self):
        """Test filter words by user."""
        form_data = {'user_id': 3}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [*range(1, 11)])

    def test_lookup_by_category(self):
        """Test filter words by category."""
        form_data = {'category': 4}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [4])

    def test_lookup_by_source(self):
        """Test filter words by source."""
        form_data = {'source': 3}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [4])

    def test_lookup_by_favorites_true(self):
        """Test filter words by only favorite words is `True`."""
        form_data = {'user_id': 3, 'favorites': True}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [3, 7])

    def test_lookup_by_favorites_false(self):
        """Test filter words by only favorite words is `False`."""
        form_data = {'user_id': 3, 'favorites': False}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [*range(1, 11)])

    @staticmethod
    def query_database(form_data):
        """Make a query to the database by form data."""
        lookup_params = LookupParams(form_data).lookup_params
        queryset = WordModel.objects.filter(
            **lookup_params
        ).values_list('id', flat=True)
        return queryset
