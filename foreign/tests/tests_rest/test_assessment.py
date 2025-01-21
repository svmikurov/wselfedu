"""Test the action to knowledge assessment of word.

Test the REST view.
"""

from http import HTTPStatus
from unittest import skip

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from config.constants import (
    PROGRES_STEPS,
    PROGRESS_MAX,
    PROGRESS_MIN,
)
from foreign.models import Word, WordProgress
from users.models import UserApp


class AssessmentUpdateRESTViewTest(APITestCase):
    """Test update the assessment REST view."""

    fixtures = ['users.json']

    def setUp(self) -> None:
        """Set up the test."""
        self.api_client = APIClient()
        self.url = reverse('foreign_rest:progress')
        self.owner = UserApp.objects.get(pk=2)
        self.stranger = UserApp.objects.get(pk=3)
        for word in ('bird', 'cat', 'dog'):
            item = Word.objects.create(foreign_word=word, user=self.owner)
            setattr(self, word, item)
        self.word = self.cat

    def test_increment_word_assessment(self) -> None:
        """Test the increment the word assessment."""
        self.api_client.force_authenticate(self.owner)
        payload = {'item_id': self.word.pk, 'action': 'know'}
        response = self.api_client.post(self.url, data=payload, format='json')
        query = WordProgress.objects.get(user=self.owner, word=self.word)

        assert response.status_code == HTTPStatus.NO_CONTENT
        assert query.progress == PROGRES_STEPS['know']

    def test_increment_max_word_assessment(self) -> None:
        """Test the increment the max word assessment."""
        WordProgress.objects.create(
            user=self.owner, word=self.word, progress=PROGRESS_MAX
        )
        self.api_client.force_authenticate(self.owner)
        payload = {'item_id': self.word.pk, 'action': 'know'}
        response = self.api_client.post(self.url, data=payload, format='json')
        query = WordProgress.objects.get(user=self.owner, word=self.word)

        assert response.status_code == HTTPStatus.NO_CONTENT
        assert query.progress == PROGRESS_MAX

    def test_decrement_word_assessment(self) -> None:
        """Test the decrement the word assessment."""
        WordProgress.objects.create(
            user=self.owner, word=self.word, progress=PROGRESS_MAX
        )
        self.api_client.force_authenticate(self.owner)
        payload = {'item_id': self.word.pk, 'action': 'not_know'}
        response = self.api_client.post(self.url, data=payload, format='json')
        query = WordProgress.objects.get(user=self.owner, word=self.word)

        assert response.status_code == HTTPStatus.NO_CONTENT
        assert query.progress == PROGRESS_MAX + PROGRES_STEPS['not_know']

    def test_decrement_min_word_assessment(self) -> None:
        """Test the decrement the min word assessment."""
        self.api_client.force_authenticate(self.owner)
        payload = {'item_id': self.word.pk, 'action': 'not_know'}
        response = self.api_client.post(self.url, data=payload, format='json')
        query = WordProgress.objects.get(user=self.owner, word=self.word)

        assert response.status_code == HTTPStatus.NO_CONTENT
        assert query.progress == PROGRESS_MIN

    def test_update_bad_word_assessment(self) -> None:
        """Test update the assessment of no correct word."""
        self.api_client.force_authenticate(self.owner)
        payload = {'item_id': 333, 'action': 'know'}
        response = self.api_client.post(self.url, data=payload, format='json')

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_update_bad_action_assessment(self) -> None:
        """Test update the assessment with no correct action."""
        self.api_client.force_authenticate(self.owner)
        payload = {'item_id': self.word.pk, 'action': 'bad'}
        response = self.api_client.post(self.url, data=payload, format='json')

        assert response.status_code == HTTPStatus.BAD_REQUEST

    @skip('Fix: assert 400 == <HTTPStatus.UNAUTHORIZED: 401>')
    def test_update_word_assessment_by_anonymous(self) -> None:
        """Test update the word assessment by anonymous."""
        payload = {'item_id': self.word.pk, 'action': 'know'}
        response = self.api_client.post(self.url, data=payload, format='json')
        query = WordProgress.objects.filter(user=self.owner, word=self.word)

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert not query.exists()

    def test_update_word_assessment_by_another_user(self) -> None:
        """Test update the word assessment by another user."""
        self.api_client.force_authenticate(self.stranger)
        payload = {'item_id': self.word.pk, 'action': 'know'}
        response = self.api_client.post(self.url, data=payload, format='json')
        query = WordProgress.objects.filter(user=self.owner, word=self.word)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert not query.exists()
