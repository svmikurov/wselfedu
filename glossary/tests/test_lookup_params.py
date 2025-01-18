"""Test the GlossaryLookupParams class."""

from datetime import datetime, timedelta

from django.conf import settings
from django.db.models import QuerySet
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
from glossary.models import Term
from glossary.queries.lookup_params import GlossaryLookupParams


class TestLookupParams(TestCase):
    """Test filter by lookup conditions.

    Test the query to database using
    :obj:`glossary.queries.lookup_params.GlossaryLookupParams`
    class and :term:`lookup_conditions` of user.
    """

    fixtures = ['tests/fixtures/users.json', 'tests/fixtures/terms.json']

    @staticmethod
    def query_database(lookup_conditions: dict[str, object]) -> QuerySet:
        """Make a query to the database by test filter."""
        lookup_params = GlossaryLookupParams(lookup_conditions).params
        queryset = Term.objects.filter(*lookup_params)
        ids = queryset.values_list('id', flat=True)
        return ids

    def test_lookup_by_user_id(self) -> None:
        """Test filter terms by user."""
        lookup_conditions = {'user_id': 2}
        queryset = self.query_database(lookup_conditions)
        self.assertQuerySetEqual(queryset, [1, 2, 3, 4, 5])

    # @skip('FIX time now')
    def test_lookup_by_date(self) -> None:
        """Test filter terms by term added date."""
        # For user_id=2 set adding term dates:
        # term with id=1 set added today
        # term with id=2 set added 3 weeks ago
        # term with id=3 set added 7 weeks ago
        # term with id=4 set added 13 weeks ago
        # term with id=5 set added 40 weeks ago
        today = datetime.now(tz=ZoneInfo(settings.TIME_ZONE))
        manager = Term.objects
        manager.filter(pk=1).update(created_at=today)
        manager.filter(pk=2).update(created_at=(today - timedelta(weeks=3)))
        manager.filter(pk=3).update(created_at=(today - timedelta(weeks=7)))
        manager.filter(pk=4).update(created_at=(today - timedelta(weeks=13)))
        manager.filter(pk=5).update(created_at=(today - timedelta(weeks=40)))

        # test no choice start period
        lookup_conditions = {'user_id': 2, 'period_start_date': NOT_CHOICES}
        queryset = self.query_database(lookup_conditions)
        self.assertQuerySetEqual(queryset, [1, 2, 3, 4, 5])

        # test choice 'today' start period
        lookup_conditions = {'user_id': 2, 'period_start_date': TODAY}
        queryset = self.query_database(lookup_conditions)
        self.assertQuerySetEqual(queryset, [1])

        # test choice '3 week ago' start period
        lookup_conditions = {'user_id': 2, 'period_start_date': WEEKS_AGO_3}
        queryset = self.query_database(lookup_conditions)
        self.assertQuerySetEqual(queryset, [1, 2])

        # test choice 'today' end period
        lookup_conditions = {'user_id': 2, 'period_end_date': TODAY}
        queryset = self.query_database(lookup_conditions)
        self.assertQuerySetEqual(queryset, [1, 2, 3, 4, 5])

        # test choice '3 week ago' end period
        lookup_conditions = {'user_id': 2, 'period_end_date': WEEKS_AGO_3}
        queryset = self.query_database(lookup_conditions)
        self.assertQuerySetEqual(queryset, [2, 3, 4, 5])

        # test choice '4 week ago' start period
        # with choice '2 week ago' end period
        lookup_conditions = {
            'user_id': 2,
            'period_start_date': WEEKS_AGO_4,
            'period_end_date': WEEKS_AGO_2,
        }
        queryset = self.query_database(lookup_conditions)
        self.assertQuerySetEqual(queryset, [2])

    def test_lookup_by_category(self) -> None:
        """Test filter terms by category."""
        lookup_conditions = {'category': 2}
        queryset = self.query_database(lookup_conditions)
        self.assertQuerySetEqual(queryset, [3])

    def test_lookup_by_progress(self) -> None:
        """Test filter terms by progress."""
        lookup_conditions = {'user_id': 2, 'progress': []}
        queryset = self.query_database(lookup_conditions)
        self.assertQuerySetEqual(queryset, [1, 2, 3, 4, 5])

        lookup_conditions = {'user_id': 2, 'progress': [STUDY]}
        queryset = self.query_database(lookup_conditions)
        self.assertQuerySetEqual(queryset, [1, 2])

        lookup_conditions = {'user_id': 2, 'progress': [STUDY, REPEAT]}
        queryset = self.query_database(lookup_conditions)
        self.assertQuerySetEqual(queryset, [1, 2, 3])

        lookup_conditions = {'user_id': 2, 'progress': [REPEAT, LEARNED]}
        queryset = self.query_database(lookup_conditions)
        self.assertQuerySetEqual(queryset, [3, 5])
