"""Database query module for Foreign word translation exercises."""

from datetime import datetime, timedelta

from django.db.models import F, Q
from zoneinfo import ZoneInfo

from config.constants import (
    COMBINATION,
    EDGE_PERIOD_ARGS,
    FAVORITES,
    NOT_CHOICES,
    ONE_WORD,
    PERIOD_END_DATE,
    PERIOD_START_DATE,
    PK,
    PROGRESS,
    STUDY,
    USER,
    USER_ID,
    WORD_COUNT,
)
from contrib.queries import LookupParams, get_q
from foreign.queries.progress import (
    PROGRESS_STAGE_EDGES,
)


class WordLookupParams(LookupParams):
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
        super().__init__(lookup_conditions)

    @property
    def params(self) -> tuple[Q, ...]:
        """Lookup parameters (`tuple[Q, ...]`, read-only)."""
        params = (
            self.user,
            self.category,
            self.source,
            self.word_date_end,
            self.word_date_start,
            self.word_favorites,
            self.word_progress,
            self.word_count,
        )
        return params

    @property
    def word_favorites(self) -> Q:
        """Lookup parameter by favorite status (`Q`, read-only)."""
        field_value = self.lookup_conditions.get(FAVORITES)
        lookup_value = self.lookup_conditions.get(USER_ID)
        lookup_field = 'wordfavorites__user_id'
        param = Q(**{lookup_field: lookup_value}) if field_value else Q()
        return param

    @property
    def word_progress(self) -> Q:
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
    def word_count(self) -> Q:
        """Lookup parameter by word count (`Q`, read-only)."""
        lookup_value = self.lookup_conditions.get(WORD_COUNT, [])
        if ONE_WORD in lookup_value or COMBINATION in lookup_value:
            lookup_value += [NOT_CHOICES]
        lookup_field = 'word_count__in'
        param = get_q(lookup_field, lookup_value)
        return param

    @property
    def word_date_start(self) -> Q:
        """Lookup parameter by word added date (`Q`, read-only)."""
        format_time = '%Y-%m-%d 00:00:00+00:00'
        lookup_value = self.get_date_value(PERIOD_START_DATE, format_time)
        lookup_field = 'created_at__gte'
        param = get_q(lookup_field, lookup_value)
        return param

    @property
    def word_date_end(self) -> Q:
        """Lookup parameter by word added date (`Q`, read-only)."""
        format_time = '%Y-%m-%d 23:59:59+00:00'
        lookup_value = self.get_date_value(PERIOD_END_DATE, format_time)
        lookup_field = 'created_at__lte'
        param = get_q(lookup_field, lookup_value)
        return param

    def get_date_value(self, period_date: str, format_time: str) -> str:
        """Get lookup date value."""
        today = datetime.now(tz=ZoneInfo('UTC'))
        period = self.lookup_conditions.get(period_date)
        period_delta = timedelta(**EDGE_PERIOD_ARGS.get(period, {}))
        end_period = today - period_delta

        lookup_value = end_period.strftime(format_time)
        date_value = lookup_value if period in EDGE_PERIOD_ARGS else ''
        return date_value
