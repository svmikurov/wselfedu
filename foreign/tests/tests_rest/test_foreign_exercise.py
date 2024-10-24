"""Test render the foreign exercise data."""

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from config.constants import (
    DEFAULT_CATEGORY,
    EXAMINATION,
    NOT_CHOICES,
    TODAY,
)
from foreign.models import Word, WordProgress
from foreign.queries.lookup_params import WordLookupParams
from users.models import UserApp


class TestRenderForeignExerciseDataREST(APITestCase):
    """Test render the foreign exercise data."""

    def setUp(self) -> None:
        """Set up the test."""
        self.api_client = APIClient()
        self.user = UserApp.objects.create(username='user')
        self.url = reverse('foreign_rest:exercise')

    def test_render_word_count(self) -> None:
        """Test render the word count info in foreign exercise."""
        self.api_client.force_authenticate(self.user)
        word = Word.objects.create(user=self.user, foreign_word='f')
        Word.objects.create(user=self.user, foreign_word='f')
        WordProgress.objects.create(user=self.user, word=word, progress=10)
        payload = {
            'period_start_date': NOT_CHOICES,
            'period_end_date': TODAY,
            'category': DEFAULT_CATEGORY,
            'progress': EXAMINATION,
        }
        response = self.api_client.post(self.url, payload, format='json')

        payload['user_id'] = self.user.id
        lookup_params = WordLookupParams(payload).params
        queryset = Word.objects.filter(*lookup_params)

        assert response.json()['item_count'] == queryset.count()
        assert response.json()['assessment'] == 10
