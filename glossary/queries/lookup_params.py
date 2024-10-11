"""Glossary exercise lookup parameters to database query."""

from datetime import datetime, timedelta

from django.conf import settings
from django.db.models import Q
from zoneinfo import ZoneInfo

from config.constants import (
    CATEGORY,
    EDGE_PERIOD_ARGS,
    PERIOD_END_DATE,
    PERIOD_START_DATE,
    PROGRESS,
    PROGRESS_STAGE_EDGES,
    USER_ID,
)
from contrib.queries import get_q


class GlossaryLookupParams:
    """Glossary exercise lookup parameters to database query.

    To get lookup parameters of class instance, use property ``params``.

    The term lookup parameters to database query for glossary exercise.
    Filters the terms by user conditions to study terms.

    :param dict[str, str | int] lookup_conditions: Lookup conditions of
     term query for Glossary exercise.

        Include fields:
            - ``'id'`` : `int`
                Parameter ``id`` stored in
                :obj:`glossary.models.GlossaryExerciseParams`
            - ``'user'`` : `int`
            - ``'progres'`` : `str` (db choice)
            - ``'category'`` : `int`
            - ``'period_start_date'`` : `str` (db choice)
            - ``'period_end_date'`` : `str` (db choice)

    """

    def __init__(self, lookup_conditions: dict) -> None:
        """Set lookup conditions."""
        self.lookup_conditions = lookup_conditions

    @property
    def params(self) -> tuple[Q, ...]:
        """Glossary exercise lookup parameters."""
        params = (
            self.user,
            self.period_start_date,
            self.period_end_date,
            self.category,
            self.progress,
        )
        return params

    @property
    def user(self) -> Q:
        """Condition to filter by user (`Q`, read-only)."""
        lookup_value = self.lookup_conditions.get(USER_ID)
        lookup_field = USER_ID
        param = get_q(lookup_field, lookup_value)
        return param

    @property
    def period_start_date(self) -> Q:
        """Start period of adding terms to glossary (`Q`, read-only)."""
        lookup_value = self._get_date_value(PERIOD_START_DATE)
        lookup_field = 'created_at__gte'
        param = get_q(lookup_field, lookup_value)
        return param

    @property
    def period_end_date(self) -> Q:
        """End period of adding terms to glossary (`Q`, read-only)."""
        lookup_value = self._get_date_value(PERIOD_END_DATE)
        lookup_field = 'created_at__lte'
        param = get_q(lookup_field, lookup_value)
        return param

    def _get_date_value(self, period_date: str) -> str:
        """Get lookup date value."""
        today = datetime.now(tz=ZoneInfo(settings.TIME_ZONE))
        period = self.lookup_conditions.get(period_date)
        period_delta = timedelta(**EDGE_PERIOD_ARGS.get(period, {}))
        end_period = today - period_delta

        lookup_value = end_period.strftime('%Y-%m-%d')
        date_value = lookup_value if period in EDGE_PERIOD_ARGS else ''
        return date_value

    @property
    def category(self) -> Q:
        """Lookup parameter by category (`Q`, read-only)."""
        lookup_value = self.lookup_conditions.get(CATEGORY)
        lookup_field = 'category_id'
        param = get_q(lookup_field, lookup_value)
        return param

    @property
    def progress(self) -> Q:
        """Lookup parameter by study progress (`Q`, read-only)."""
        lookup_aliases = self.lookup_conditions.get(PROGRESS, [])
        lookup_value = self._to_numeric(PROGRESS_STAGE_EDGES, lookup_aliases)
        lookup_field = 'progress__in'
        param = get_q(lookup_field, lookup_value)
        return param

    @staticmethod
    def _to_numeric(assessments: dict, string_values: list) -> list[int]:
        """Convert a literal representation of progress.

        Convert a literal representation of an assessment into a list
        of numeric values.
        """
        numeric_values = []
        for assessment in string_values:
            numeric_values += assessments.get(assessment, [])
        return numeric_values
