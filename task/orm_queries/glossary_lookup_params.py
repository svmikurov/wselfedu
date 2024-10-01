"""Glossary exercise lookup parameters to database query."""

import datetime

from django.db.models import Q

from config.constants import EDGE_PERIOD_ARGS
from english.orm_queries.word_knowledge_assessment import PROGRESS_STAGE_EDGES


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
        lookup_value = self.lookup_conditions.get('user_id')
        lookup_field = 'user_id'
        param = Q(**{lookup_field: lookup_value}) if lookup_value else Q()
        return param

    @property
    def period_start_date(self) -> Q:
        """Start period of adding terms to glossary (`Q`, read-only)."""
        period_date = 'period_start_date'
        format_date = '%Y-%m-%d'
        lookup_value = self._get_date_value(period_date, format_date)
        lookup_field = 'created_at__gte'
        param = Q(**{lookup_field: lookup_value}) if lookup_value else Q()
        return param

    @property
    def period_end_date(self) -> Q:
        """End period of adding terms to glossary (`Q`, read-only)."""
        period_date = 'period_end_date'
        format_date = '%Y-%m-%d'
        lookup_value = self._get_date_value(period_date, format_date)
        lookup_field = 'created_at__lte'
        param = Q(**{lookup_field: lookup_value}) if lookup_value else Q()
        return param

    def _get_date_value(self, period_date: str, format_time: str) -> str:
        """Get lookup date value."""
        day_today = datetime.datetime.now(tz=datetime.timezone.utc)
        period = self.lookup_conditions.get(period_date)
        period_delta = datetime.timedelta(**EDGE_PERIOD_ARGS.get(period, {}))
        end_period = day_today - period_delta

        lookup_value = end_period.strftime(format_time)
        date_value = lookup_value if period in EDGE_PERIOD_ARGS else ''
        return date_value

    @property
    def category(self) -> Q:
        """Lookup parameter by category (`Q`, read-only)."""
        lookup_value = self.lookup_conditions.get('category')
        lookup_field = 'category_id'
        param = Q(**{lookup_field: lookup_value}) if lookup_value else Q()
        return param

    @property
    def progress(self) -> Q:
        """Lookup parameter by study progress (`Q`, read-only)."""
        lookup_aliases = self.lookup_conditions.get('progress', [])
        lookup_value = self._to_numeric(PROGRESS_STAGE_EDGES, lookup_aliases)
        lookup_field = 'progress__in'
        param = Q(**{lookup_field: lookup_value}) if lookup_value else Q()
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
