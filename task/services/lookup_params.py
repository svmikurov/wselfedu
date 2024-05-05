from django.db.models import F


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
        return {
            **self._user,
            **self._favorite_lookup_param,
            **self._category_lookup_param,
            **self._source_lookup_param,
            **self._knowledge_assessment,
        }

    @property
    def _user(self):
        """Lookup parameter by user."""
        lookup_value = self.form_data.get('user_id')
        lookup_field = 'user'
        return {lookup_field: lookup_value} if lookup_value else {}

    @property
    def _favorite_lookup_param(self):
        """Lookup parameter by favorite status."""
        fild_value = self.form_data.get('favorites')
        if fild_value:
            lookup_value = self.form_data.get('user_id')
            lookup_field = 'wordsfavoritesmodel__user_id'
            lookup_param = {lookup_field: lookup_value}
            return lookup_param
        return {}

    @property
    def _category_lookup_param(self):
        """Lookup parameter by category."""
        lookup_value = self.form_data.get('category')
        lookup_field = 'category_id'
        return {lookup_field: lookup_value} if lookup_value else {}

    @property
    def _source_lookup_param(self):
        """Lookup parameter by source."""
        lookup_value = self.form_data.get('source')
        lookup_field = 'source_id'
        return {lookup_field: lookup_value} if lookup_value else {}

    @property
    def _knowledge_assessment(self):
        """Lookup parameter by user knowledge assessment."""
        form_value = self.form_data.get('knowledge_assessment', {})
        if not form_value:
            return {}

        lookup_value = self._to_numeric(self.ASSESSMENTS, form_value)
        lookup_field = 'worduserknowledgerelation__knowledge_assessment__in'
        if lookup_value:
            return {
                lookup_field: lookup_value,
                'worduserknowledgerelation__word_id': F('pk'),
            }
        return {}

    @staticmethod
    def _to_numeric(assessments, string_values):
        """Convert a literal representation of an assessment into a list of
        numeric values.
        """
        numeric_values = []
        for assessment in string_values:
            numeric_values += assessments.get(assessment, [])
        return numeric_values
