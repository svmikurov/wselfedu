from django.test import Client, TestCase

from english.views.analitical_queries.analysis_data import (
    get_favorites_analytic_data,
)


class TestFavoritesQuery(TestCase):
    """"""

    fixtures = ['english/tests/fixtures/wse-fixtures-4.json']

    def setUp(self):
        """Set up data."""
        self.client = Client()
        self.user_id = 3

        self.all_favorites_user_count = 2
        self.study_favorites_user_count = 1

    def test_favorites_user_count_qs(self):
        """Test the queryset for counting the user's favorite words."""
        qs = get_favorites_analytic_data(self.user_id)
        assert self.all_favorites_user_count == qs['count_favorites']

    def test_study_favorites_user_count_qs(self):
        """Test study favorites user word count."""
        qs = get_favorites_analytic_data(self.user_id)
        assert self.study_favorites_user_count == qs['study_favorites']
