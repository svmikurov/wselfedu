"""Database query module for Foreign word translation exercises."""

import datetime

from django.db.models import F, Q

from config.constants import (
    CATEGORY,
    COMBINATION,
    EDGE_PERIOD_ARGS,
    FAVORITES,
    NOT_CHOICES,
    ONE_WORD,
    PERIOD_END_DATE,
    PERIOD_START_DATE,
    PK,
    PROGRESS,
    SOURCE,
    STUDY,
    USER,
    USER_ID,
    WORD_COUNT,
)
from foreign.queries.progress import (
    PROGRESS_STAGE_EDGES,
)


class LookupParams:
    """Lookup parameters class.

    :param dict lookup_conditions: The user exercise conditions.

    Examples
    --------
    .. code-block:: python

        lookup_params = LookupParams(lookup_conditions)
        params: tuple[Q, ...] = lookup_params.params
        query = Model.objects.filter(*params)

    """

    def __init__(self, lookup_conditions: dict) -> None:
        """Lookup parameters constructor."""
        self.lookup_conditions = lookup_conditions

    @property
    def params(self) -> tuple[Q, ...]:
        """Lookup parameters (`tuple[Q, ...]`, read-only)."""
        params = (
            self._user_lookup_param,
            self._favorites_lookup_param,
            self._category_lookup_param,
            self._source_lookup_param,
            self._knowledge_lookup_param,
            self._word_count_lookup_param,
            self._date_start_lookup_param,
            self._date_end_lookup_param,
        )
        return params

    @property
    def _user_lookup_param(self) -> Q:
        """Lookup parameter by user (`Q`, read-only)."""
        lookup_value = self.lookup_conditions.get(USER_ID)
        lookup_field = USER
        param = Q(**{lookup_field: lookup_value}) if lookup_value else Q()
        return param

    @property
    def _favorites_lookup_param(self) -> Q:
        """Lookup parameter by favorite status (`Q`, read-only)."""
        field_value = self.lookup_conditions.get(FAVORITES)
        lookup_value = self.lookup_conditions.get(USER_ID)
        lookup_field = 'wordfavorites__user_id'
        param = Q(**{lookup_field: lookup_value}) if field_value else Q()
        return param

    @property
    def _category_lookup_param(self) -> Q:
        """Lookup parameter by category (`Q`, read-only)."""
        lookup_value = self.lookup_conditions.get(CATEGORY)
        lookup_field = 'category_id'
        param = Q(**{lookup_field: lookup_value}) if lookup_value else Q()
        return param

    @property
    def _source_lookup_param(self) -> Q:
        """Lookup parameter by source (`Q`, read-only)."""
        lookup_value = self.lookup_conditions.get(SOURCE)
        lookup_field = 'source_id'
        param = Q(**{lookup_field: lookup_value}) if lookup_value else Q()
        return param

    @property
    def _knowledge_lookup_param(self) -> Q:
        """Lookup parameter by user assessment (`Q`, read-only)."""
        form_value = self.lookup_conditions.get(PROGRESS, [])
        lookup_value = self._to_numeric(PROGRESS_STAGE_EDGES, form_value)
        lookup_field = 'wordprogress__progress__in'

        words_with_assessment = Q(**{lookup_field: lookup_value})
        words_without_assessment = Q(user_id=F(USER)) & ~Q(
            wordprogress__user_id=F(USER),
            wordprogress__word_id=F(PK),
        )

        if lookup_value:
            if STUDY in form_value:
                param = words_with_assessment | words_without_assessment
            else:
                param = words_with_assessment
        else:
            param = Q()

        return param

    @property
    def _word_count_lookup_param(self) -> Q:
        """Lookup parameter by word count (`Q`, read-only)."""
        lookup_value = self.lookup_conditions.get(WORD_COUNT, [])
        if ONE_WORD in lookup_value or COMBINATION in lookup_value:
            lookup_value += [NOT_CHOICES]
        lookup_field = 'word_count__in'
        param = Q(**{lookup_field: lookup_value}) if lookup_value else Q()
        return param

    @property
    def _date_start_lookup_param(self) -> Q:
        """Lookup parameter by word added date (`Q`, read-only)."""
        period_date = PERIOD_START_DATE
        format_time = '%Y-%m-%d 00:00:00+00:00'
        lookup_value = self._get_date_value(period_date, format_time)
        lookup_field = 'created_at__gte'
        param = Q(**{lookup_field: lookup_value}) if lookup_value else Q()
        return param

    @property
    def _date_end_lookup_param(self) -> Q:
        """Lookup parameter by word added date (`Q`, read-only)."""
        period_date = PERIOD_END_DATE
        format_time = '%Y-%m-%d 23:59:59+00:00'
        lookup_value = self._get_date_value(period_date, format_time)
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
