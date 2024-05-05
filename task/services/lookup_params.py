import datetime

from django.db.models import F, Q

EDGE_PERIODS = {
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


class LookupParams:
    """Lookup parameters class."""

    ASSESSMENTS = {
        'S': [0, 1, 2, 3, 4, 5, 6],
        'R': [7, 8],
        'E': [9, 10],
        'K': [11],
    }

    def __init__(self, form_data):
        self.form_data = form_data

    @property
    def lookup_params(self):
        """lookup parameters."""
        return (
            self._user,
            self._favorite,
            self._category,
            self._source,
            self._knowledge,
            self._date_start,
            self._date_end,
        )

    @property
    def _user(self):
        """Lookup parameter by user."""
        lookup_value = self.form_data.get('user_id')
        return Q(user=lookup_value) if lookup_value else Q()

    @property
    def _favorite(self):
        """Lookup parameter by favorite status."""
        field_value = self.form_data.get('favorites')
        lookup_value = self.form_data.get('user_id')
        lookup_field = 'wordsfavoritesmodel__user_id'
        return Q(**{lookup_field: lookup_value}) if field_value else Q()

    @property
    def _category(self):
        """Lookup parameter by category."""
        lookup_value = self.form_data.get('category')
        return Q(category_id=lookup_value) if lookup_value else Q()

    @property
    def _source(self):
        """Lookup parameter by source."""
        lookup_value = self.form_data.get('source')
        return Q(source_id=lookup_value) if lookup_value else Q()

    @property
    def _knowledge(self):
        """Lookup parameter by user knowledge assessment."""
        form_value = self.form_data.get('knowledge_assessment', {})
        lookup_value = self._to_numeric(self.ASSESSMENTS, form_value)
        lookup_field = 'worduserknowledgerelation__knowledge_assessment__in'

        words_with_assessment = Q(**{lookup_field: lookup_value})
        words_without_assessment = (
            Q(user_id=F('user'))
            & ~Q(
                worduserknowledgerelation__user_id=F('user'),
                worduserknowledgerelation__word_id=F('pk'),
            )
        )

        if lookup_value and 'S' in form_value:
            return words_with_assessment | words_without_assessment
        elif lookup_value:
            return words_with_assessment
        else:
            return Q()

    @property
    def _date_start(self):
        """Lookup parameter by word added date."""
        period_date = 'period_start_date'
        format_time = '%Y-%m-%d 00:00:00+00:00'
        lookup_value = self._gat_date_value(period_date, format_time)
        return Q(created_at__gte=lookup_value) if lookup_value else Q()

    @property
    def _date_end(self):
        """Lookup parameter by word added date."""
        period_date = 'period_end_date'
        format_time = '%Y-%m-%d 23:59:59+00:00'
        lookup_value = self._gat_date_value(period_date, format_time)
        return Q(created_at__lte=lookup_value) if lookup_value else Q()

    def _gat_date_value(self, period_date, format_time):
        """Get lookup date value."""
        day_today = datetime.datetime.now(tz=datetime.timezone.utc)
        period = self.form_data.get(period_date)
        period_delta = datetime.timedelta(**EDGE_PERIODS.get(period, {}))
        end_period = day_today - period_delta

        lookup_value = end_period.strftime(format_time)
        return lookup_value if period in EDGE_PERIODS else {}

    @staticmethod
    def _to_numeric(assessments, string_values):
        """Convert a literal representation of an assessment into a list of
        numeric values.
        """
        numeric_values = []
        for assessment in string_values:
            numeric_values += assessments.get(assessment, [])
        return numeric_values
