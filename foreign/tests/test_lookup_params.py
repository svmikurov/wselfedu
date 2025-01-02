"""Test lookup params for word study task."""

from datetime import datetime, timedelta

from django.conf import settings
from django.db.models.query import QuerySet
from django.test import TestCase
from zoneinfo import ZoneInfo

from config.constants import (
    LEARNED,
    NOT_CHOICES,
    REPEAT,
    STUDY,
    TODAY,
    WEEKS_AGO_2,
    WEEKS_AGO_3,
    WEEKS_AGO_4,
)
from foreign.models import Word
from foreign.queries.lookup_params import WordLookupParams


class LookupParamsTest(TestCase):
    """Test get Word Queryset by user parameters."""

    fixtures = ['tests/fixtures/foreign.json', 'tests/fixtures/users.json']

    @classmethod
    def setUp(cls) -> None:
        """Set up database data."""

    def test_lookup_by_user_id(self) -> None:
        """Test filter words by user."""
        form_data = {'user_id': 3}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [*range(1, 11)])

    def test_lookup_by_category(self) -> None:
        """Test filter words by category."""
        form_data = {'category': 4}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [4])

    def test_lookup_by_source(self) -> None:
        """Test filter words by source."""
        form_data = {'source': 3}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [4])

    def test_lookup_by_favorites_true(self) -> None:
        """Test filter words by only favorite words is `True`."""
        form_data = {'user_id': 3, 'favorites': True}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [3, 7])

    def test_lookup_by_favorites_false(self) -> None:
        """Test filter words by only favorite words is `False`."""
        form_data = {'user_id': 3, 'favorites': False}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [*range(1, 11)])

    def test_lookup_by_progress(self) -> None:
        """Test filter words by word knowledge assessment."""
        form_data = {'user_id': 3, 'progress': []}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [*range(1, 11)])

        form_data = {'user_id': 3, 'progress': [STUDY]}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [1, 2, 3, 4, 10])

        form_data = {'user_id': 3, 'progress': [STUDY, REPEAT]}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [1, 2, 3, 4, 5, 6, 10])

        form_data = {'user_id': 3, 'progress': [REPEAT, LEARNED]}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [5, 6, 9])

    def test_lookup_by_date(self) -> None:
        """Test filter words by word added date."""
        # test no choice start period
        today = datetime.now(tz=ZoneInfo(settings.TIME_ZONE))
        manager = Word.objects
        manager.filter(pk=1).update(created_at=today)
        manager.filter(pk=2).update(created_at=(today - timedelta(weeks=3)))

        # test no choice start period
        form_data = {'user_id': 3, 'period_start_date': NOT_CHOICES}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [*range(1, 11)])

        # test choice 'today' start period
        form_data = {'user_id': 3, 'period_start_date': TODAY}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [1])

        # test choice '3 week ago' start period
        form_data = {'user_id': 3, 'period_start_date': WEEKS_AGO_3}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [1, 2])

        # test choice 'today' end period
        form_data = {'user_id': 3, 'period_end_date': TODAY}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [*range(1, 11)])

        # test choice '3 week ago' end period
        form_data = {'user_id': 3, 'period_end_date': WEEKS_AGO_3}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [*range(2, 11)])

        # test choice '4 week ago' start period
        # with choice '2 week ago' end period
        form_data = {
            'user_id': 3,
            'period_start_date': WEEKS_AGO_4,
            'period_end_date': WEEKS_AGO_2,
        }
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [2])

    @staticmethod
    def query_database(form_data: dict[str, object]) -> QuerySet:
        """Make a query to the database by form data."""
        lookup_params = WordLookupParams(form_data).params
        queryset = Word.objects.filter(*lookup_params)
        ids = queryset.values_list('id', flat=True)
        return ids
