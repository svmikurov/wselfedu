from datetime import datetime, timezone, timedelta

from django.test import TestCase

from english.models import WordModel
from task.services import LookupParams


class LookupParamsTest(TestCase):
    """Test get Word Queryset by user parameters."""

    fixtures = ['task/tests/fixtures/wse-fixtures-4.json']

    @classmethod
    def setUp(cls):
        """Set up database data."""

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

    def test_lookup_by_knowledge_assessment(self):
        """Test filter words by word knowledge assessment."""
        form_data = {'user_id': 3, 'knowledge_assessment': []}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [*range(1, 11)])

        form_data = {'user_id': 3, 'knowledge_assessment': ['S']}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [1, 2, 3, 4, 10])

        form_data = {'user_id': 3, 'knowledge_assessment': ['S', 'R']}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [1, 2, 3, 4, 5, 6, 10])

        form_data = {'user_id': 3, 'knowledge_assessment': ['R', 'K']}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [5, 6, 9])

    def test_lookup_by_word_count(self):
        """Test filter words by word count."""
        # no choice
        form_data = {'user_id': 3, 'word_count': []}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [*range(1, 11)])

        # 'Слово', 'Словосочетание' in condition
        form_data = {'user_id': 3, 'word_count': ['OW', 'CB']}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [1, 2, 3, 6, 7, 8, 9, 10])

        # 'Предложение' in condition
        form_data = {'user_id': 3, 'word_count': ['ST']}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [5])

    def test_lookup_by_date(self):
        """Test filter words by word added date."""
        # test no choice start period
        today = datetime.now(tz=timezone.utc)
        manager = WordModel.objects
        manager.filter(pk=1).update(created_at=today)
        manager.filter(pk=2).update(created_at=(today - timedelta(weeks=3)))

        # test no choice start period
        form_data = {'user_id': 3, 'period_start_date': 'NC'}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [*range(1, 11)])

        # test choice 'today' start period
        form_data = {'user_id': 3, 'period_start_date': 'DT'}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [1])

        # test choice '3 week ago' start period
        form_data = {'user_id': 3, 'period_start_date': 'W3'}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [1, 2])

        # test choice 'today' end period
        form_data = {'user_id': 3, 'period_end_date': 'DT'}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [*range(1, 11)])

        # test choice '3 week ago' end period
        form_data = {'user_id': 3, 'period_end_date': 'W3'}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [*range(2, 11)])

        # test choice '4 week ago' start period
        # with choice '2 week ago' end period
        form_data = {
            'user_id': 3,
            'period_start_date': 'W4',
            'period_end_date': 'W2',
        }
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [2])

    @staticmethod
    def query_database(form_data):
        """Make a query to the database by form data."""
        lookup_params = LookupParams(form_data).params
        queryset = WordModel.objects.filter(
            *lookup_params
        )
        queryset = queryset.values_list('id', flat=True)
        return queryset
