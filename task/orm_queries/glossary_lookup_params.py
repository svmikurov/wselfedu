"""Glossary exercise query."""

import datetime

from django.db.models import Q, F

from config.consts import PROGRES_STAGE_ALIASES

EDGE_PERIODS_TERMS = {
    'DT': {'days': 0},
    'D3': {'days': 3},
    'W1': {'weeks': 1},
    'W2': {'weeks': 2},
    'W3': {'weeks': 3},
    'W4': {'weeks': 4},
    'W7': {'weeks': 7},
    'M3': {'weeks': 13},
    'M6': {'weeks': 26},
    'M9': {'weeks': 40},
}
"""The term representation of period aliases at word adding for study
(`dict[str, dict[str, int]]`).

key : `str`
    Period alias at word adding for study.
value : `dict[str, int]]`
    Period of time at word adding for study.
        key : `str`
            The ``datetime.timedelta`` function argument name.
        value : `int`
            The ``datetime.timedelta`` function argument value.
"""


class GlossaryExerciseLookupParams:
    """Glossary exercise lookup parameters.

    Lookup parameters
    -----------------
    lookup_params : `dict[str, str | int]`
        Lookup parameters of term query for Glossary exercise.

        - ``'id'`` : `int`
            Params id in ``GlossaryExerciseParams``
        - ``'user'`` : `int`
        - ``'progres'`` : `str` (db choice)
        - ``'category'`` : `int`
        - ``'period_start_date'`` : `str`

        - ``'period_end_date'`` : `str` (db choice)

    """

    def __init__(self, lookup_conditions: dict) -> None:
        """Construct the query."""
        self.lookup_conditions = lookup_conditions

    @property
    def params(self) -> tuple[Q, ...]:
        """Glossary exercise lookup params."""
        params = (
            self.user,
            self.period_start_date,
            self.period_end_date,
            self.category,
            self.progres,
        )
        return params

    def user(self) -> Q:
        """User lookup (`Q`, read-only)."""
        lookup_value = self.lookup_conditions.get('user_id')
        lookup_field = 'user'
        param = Q(**{lookup_field: lookup_value}) if lookup_value else Q()
        return param

    @property
    def period_start_date(self) -> Q:
        """Lookup parameter by user (`Q`, read-only)."""
        period_date = 'period_start_date'
        format_time = '%Y-%m-%d 00:00:00+00:00'
        lookup_value = self._get_date_value(period_date, format_time)
        lookup_field = 'created_at__gte'
        param = Q(**{lookup_field: lookup_value}) if lookup_value else Q()
        return param

    @property
    def period_end_date(self) -> Q:
        """Lookup parameter by word added date (`Q`, read-only)."""
        period_date = 'period_end_date'
        format_time = '%Y-%m-%d 23:59:59+00:00'
        lookup_value = self._get_date_value(period_date, format_time)
        lookup_field = 'created_at__lte'
        param = Q(**{lookup_field: lookup_value}) if lookup_value else Q()
        return param

    @property
    def category(self) -> Q:
        """Lookup parameter by category (`Q`, read-only)."""
        lookup_value = self.lookup_conditions.get('category')
        lookup_field = 'category_id'
        param = Q(**{lookup_field: lookup_value}) if lookup_value else Q()
        return param

    @property
    def progres(self) -> Q:
        """Lookup parameter by user assessment (`Q`, read-only)."""
        form_value = self.lookup_conditions.get('knowledge_assessment', [])
        lookup_value = self._to_numeric(PROGRES_STAGE_ALIASES, form_value)
        lookup_field = 'worduserknowledgerelation__knowledge_assessment__in'

        words_with_assessment = Q(**{lookup_field: lookup_value})
        words_without_assessment = Q(user_id=F('user')) & ~Q(
            worduserknowledgerelation__user_id=F('user'),
            worduserknowledgerelation__word_id=F('pk'),
        )

        if lookup_value:
            if 'S' in form_value:
                param = words_with_assessment | words_without_assessment
            else:
                param = words_with_assessment
        else:
            param = Q()

        return param

    def _get_date_value(self, period_date: str, format_time: str) -> str:
        """Get lookup date value."""
        day_today = datetime.datetime.now(tz=datetime.timezone.utc)
        period = self.lookup_conditions.get(period_date)
        period_delta = datetime.timedelta(**EDGE_PERIODS_TERMS.get(period, {}))
        end_period = day_today - period_delta

        lookup_value = end_period.strftime(format_time)
        date_value = lookup_value if period in EDGE_PERIODS_TERMS else ''
        return date_value

    @staticmethod
    def _to_numeric(assessments: dict, string_values: list) -> list[int]:
        """Convert a literal representation of an assessment.

        Convert a literal representation of an assessment into a list
        of numeric values.
        """
        numeric_values = []
        for assessment in string_values:
            numeric_values += assessments.get(assessment, [])
        return numeric_values
