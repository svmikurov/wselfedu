"""Test render the foreign exercise data."""

from http import HTTPStatus
from unittest import skip

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
        word = Word.objects.create(user=self.user, foreign_word='a')
        Word.objects.create(user=self.user, foreign_word='b')
        WordProgress.objects.create(user=self.user, word=word, progress=10)
        payload = {
            'period_start_date': NOT_CHOICES,
            'period_end_date': TODAY,
            'category': DEFAULT_CATEGORY,
            'progress': EXAMINATION,
        }
        response = self.api_client.post(self.url, payload, 'json')

        payload['user_id'] = self.user.id
        lookup_params = WordLookupParams(payload).params
        queryset = Word.objects.filter(*lookup_params)

        assert response.json()['item_count'] == queryset.count()
        assert response.json()['assessment'] == 10

    def test_first_count(self) -> None:
        """Test study first word count at exercise params."""
        word_count_param = 33
        word_count = 100
        for num in range(word_count):
            Word.objects.create(user=self.user, foreign_word=f'word_{num}')
        payload = {
            'count_first': word_count_param,
        }
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(self.url, payload)

        assert response.status_code == HTTPStatus.OK
        assert response.json()['item_count'] == word_count_param

    @skip
    def test_last_count(self) -> None:
        """Test study first word count at exercise params."""
        word_count_param = 33
        word_count = 100
        for num in range(word_count):
            Word.objects.create(user=self.user, foreign_word=f'word_{num}')
        payload = {
            'count_last': word_count_param,
        }
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(self.url, payload)

        assert response.status_code == HTTPStatus.OK
        assert response.json()['item_count'] == word_count_param
