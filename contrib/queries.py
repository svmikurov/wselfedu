"""General ORM queries."""

import abc
from datetime import datetime, timedelta

from django.db.models import Q
from zoneinfo import ZoneInfo

from config import settings
from config.constants import (
    EDGE_PERIOD_ARGS,
    PROGRESS_STAGE_EDGES,
)


class LookupParams(abc.ABC):
    """Base lookup parameters."""

    def __init__(self, lookup_conditions: dict) -> None:
        """Set lookup conditions."""
        self.lookup_conditions = lookup_conditions

    @abc.abstractmethod
    def params(self) -> tuple[Q, ...]:
        """Lookup params (tuple[Q, ...], read-only).

        Override to return a sequence of required condition properties.
        """
        pass

    @property
    def user(self) -> Q:
        """Condition to filter by user (`Q`, read-only)."""
        lookup_value = self.lookup_conditions.get('user_id')
        lookup_field = 'user'
        param = get_q(lookup_field, lookup_value)
        return param

    @property
    def period_start_date(self) -> Q:
        """Start period of adding items to database (`Q`, read-only)."""
        lookup_value = self._get_date_value('period_start_date')
        lookup_field = 'created_at__gte'
        param = get_q(lookup_field, lookup_value)
        return param

    @property
    def period_end_date(self) -> Q:
        """End period of adding items to database (`Q`, read-only)."""
        lookup_value = self._get_date_value('period_end_date')
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
        lookup_value = self.lookup_conditions.get('category')
        lookup_field = 'category_id'
        param = get_q(lookup_field, lookup_value)
        return param

    @property
    def source(self) -> Q:
        """Lookup parameter by source (`Q`, read-only)."""
        lookup_value = self.lookup_conditions.get('source')
        lookup_field = 'source_id'
        param = get_q(lookup_field, lookup_value)
        return param

    @property
    def progress(self) -> Q:
        """Lookup parameter by study progress (`Q`, read-only)."""
        lookup_aliases = self.lookup_conditions.get('progress', [])
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


def get_q(lookup_field: str, lookup_value: object) -> Q:
    """Get SQL condition representation."""
    return Q(**{lookup_field: lookup_value}) if lookup_value else Q()
