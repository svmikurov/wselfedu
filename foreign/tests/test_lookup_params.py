"""Test lookup params for word study task."""

from datetime import datetime, timedelta

from django.conf import settings
from django.db.models.query import QuerySet
from django.test import TestCase
from zoneinfo import ZoneInfo

from config.constants import (
    CATEGORY,
    COMBINATION,
    FAVORITES,
    ID,
    LEARNED,
    NOT_CHOICES,
    ONE_WORD,
    PERIOD_END_DATE,
    PERIOD_START_DATE,
    PROGRESS,
    REPEAT,
    SENTENCE,
    SOURCE,
    STUDY,
    TODAY,
    USER_ID,
    WEEKS_AGO_2,
    WEEKS_AGO_3,
    WEEKS_AGO_4,
    WORD_COUNT,
)
from foreign.models import Word
from foreign.queries.lookup_params import WordLookupParams


class LookupParamsTest(TestCase):
    """Test get Word Queryset by user parameters."""

    fixtures = ['foreign/tests/fixtures/wse-fixtures-4.json']

    @classmethod
    def setUp(cls) -> None:
        """Set up database data."""

    def test_lookup_by_user_id(self) -> None:
        """Test filter words by user."""
        form_data = {USER_ID: 3}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [*range(1, 11)])

    def test_lookup_by_category(self) -> None:
        """Test filter words by category."""
        form_data = {CATEGORY: 4}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [4])

    def test_lookup_by_source(self) -> None:
        """Test filter words by source."""
        form_data = {SOURCE: 3}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [4])

    def test_lookup_by_favorites_true(self) -> None:
        """Test filter words by only favorite words is `True`."""
        form_data = {USER_ID: 3, FAVORITES: True}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [3, 7])

    def test_lookup_by_favorites_false(self) -> None:
        """Test filter words by only favorite words is `False`."""
        form_data = {USER_ID: 3, FAVORITES: False}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [*range(1, 11)])

    def test_lookup_by_progress(self) -> None:
        """Test filter words by word knowledge assessment."""
        form_data = {USER_ID: 3, PROGRESS: []}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [*range(1, 11)])

        form_data = {USER_ID: 3, PROGRESS: [STUDY]}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [1, 2, 3, 4, 10])

        form_data = {USER_ID: 3, PROGRESS: [STUDY, REPEAT]}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [1, 2, 3, 4, 5, 6, 10])

        form_data = {USER_ID: 3, PROGRESS: [REPEAT, LEARNED]}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [5, 6, 9])

    def test_lookup_by_word_count(self) -> None:
        """Test filter words by word count."""
        # no choice
        form_data = {USER_ID: 3, WORD_COUNT: []}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [*range(1, 11)])

        # 'Слово', 'Словосочетание' in condition
        form_data = {USER_ID: 3, WORD_COUNT: [ONE_WORD, COMBINATION]}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [1, 2, 3, 6, 7, 8, 9, 10])

        # 'Предложение' in condition
        form_data = {USER_ID: 3, WORD_COUNT: [SENTENCE]}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [5])

    def test_lookup_by_date(self) -> None:
        """Test filter words by word added date."""
        # test no choice start period
        today = datetime.now(tz=ZoneInfo(settings.TIME_ZONE))
        manager = Word.objects
        manager.filter(pk=1).update(created_at=today)
        manager.filter(pk=2).update(created_at=(today - timedelta(weeks=3)))

        # test no choice start period
        form_data = {USER_ID: 3, PERIOD_START_DATE: NOT_CHOICES}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [*range(1, 11)])

        # test choice 'today' start period
        form_data = {USER_ID: 3, PERIOD_START_DATE: TODAY}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [1])

        # test choice '3 week ago' start period
        form_data = {USER_ID: 3, PERIOD_START_DATE: WEEKS_AGO_3}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [1, 2])

        # test choice 'today' end period
        form_data = {USER_ID: 3, PERIOD_END_DATE: TODAY}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [*range(1, 11)])

        # test choice '3 week ago' end period
        form_data = {USER_ID: 3, PERIOD_END_DATE: WEEKS_AGO_3}
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [*range(2, 11)])

        # test choice '4 week ago' start period
        # with choice '2 week ago' end period
        form_data = {
            USER_ID: 3,
            PERIOD_START_DATE: WEEKS_AGO_4,
            PERIOD_END_DATE: WEEKS_AGO_2,
        }
        queryset = self.query_database(form_data)
        self.assertQuerySetEqual(queryset, [2])

    @staticmethod
    def query_database(form_data: dict[str, object]) -> QuerySet:
        """Make a query to the database by form data."""
        lookup_params = WordLookupParams(form_data).params
        queryset = Word.objects.filter(*lookup_params)
        ids = queryset.values_list(ID, flat=True)
        return ids
