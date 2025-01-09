"""Test fix the render the same task.

.. code-block:: python
   :caption: Foreign exercise lookup_conditions:

    lookup_conditions = {
        'period_start_date': 'NC',
        'period_end_date': 'DT',
        'category': None,
        'progress': 'S',
        'user_id': 3,
        'timeout': 5,
        'order': 'TR'
    }
    # renders only 'word_u3_w10' word
"""

from unittest import skip

from django.db.models import QuerySet
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from foreign.models import Word
from foreign.queries.lookup_params import WordLookupParams
from users.models import UserApp


class RenderSameTaskTest(APITestCase):
    """Foreign exercise render same ford test."""

    fixtures = ['foreign.json', 'terms.json', 'users.json', 'words.json']

    def setUp(self) -> None:
        """Set up test data."""
        self.api_client = APIClient()
        self.user = UserApp.objects.get(pk=3)
        self.url = reverse('foreign_rest:exercise')
        self.params = {
            'period_start_date': 'NC',
            'period_end_date': 'DT',
            'category': None,
            'progress': ['S'],
        }

    @skip
    def test_reproduce_issue(self) -> None:
        """Test the reproduce issue."""
        self.api_client.force_authenticate(self.user)
        response = self.api_client.post(self.url, self.params, format='json')
        payload = response.json()  # noqa: F841

    @skip
    def test_params_to_word_lookup_params(self) -> None:
        """Test params."""

    @staticmethod
    def query_database(data: dict[str, object]) -> QuerySet:
        """Make a query to the database by form data."""
        lookup_params = WordLookupParams(data).params
        queryset = Word.objects.filter(*lookup_params)
        return queryset
