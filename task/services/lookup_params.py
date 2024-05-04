from django.db.models import F


class LookupParams:
    """Lookup parameters class."""

    ASSESSMENTS = {
        'S': [*range(7)],
        'R': [7, 8],
        'E': [9, 11],
        'K': [11],
    }

    def __init__(self, form_data):
        self.form_data = form_data

    @property
    def lookup_params(self):
        """lookup parameters."""
        return {
            **self._user,
            **self._category_lookup_param,
            **self._source_lookup_param,
            **self._favorite_lookup_param,
            # **self._knowledge_assessment,
        }

    @property
    def _user(self):
        """Lookup parameter by user."""
        lookup_value = self.form_data.get('user_id')
        lookup_field = 'user'
        lookup_param = {lookup_field: lookup_value} if lookup_value else {}
        return lookup_param

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
        lookup_param = {lookup_field: lookup_value} if lookup_value else {}
        return lookup_param

    @property
    def _source_lookup_param(self):
        """Lookup parameter by source."""
        lookup_value = self.form_data.get('source')
        lookup_field = 'source_id'
        lookup_param = {lookup_field: lookup_value} if lookup_value else {}
        return lookup_param

    @property
    def _knowledge_assessment(self):
        """Lookup parameter by user knowledge assessment."""
        form_value = self.form_data.get('knowledge_assessment')
        lookup_value = self._to_numeric_assessment(self.ASSESSMENTS, form_value)
        lookup_field = 'worduserknowledgerelation__knowledge_assessment__in'
        lookup_param = {lookup_field: lookup_value} if lookup_value else {}
        if lookup_param:
            return {
                **lookup_param,
                'worduserknowledgerelation__word_id': F('pk'),
            }
        return {}

    @staticmethod
    def _to_numeric_assessment(assessments, string_values):
        """Convert a literal representation of an assessment into a list of
        numeric values.
        """
        numeric_values = []
        for assessment in string_values:
            numeric_values += assessments[assessment]
        return numeric_values
