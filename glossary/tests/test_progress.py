"""Test update term study progress view."""

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from config.constants import (
    DECREMENT_STEP,
    INCREMENT_STEP,
    PROGRESS_MAX,
    PROGRESS_MIN,
)
from glossary.models import Term
from users.models import UserApp


class TestUpdateProgressView(APITestCase):
    """Test update term study progress view.

    Test the :py:meth:`glossary.views_drf.update_term_study_progress`
    view.
    """

    fixtures = ['tests/fixtures/users.json', 'tests/fixtures/terms.json']

    def setUp(self) -> None:
        """Set up test data."""
        self.api_client = APIClient()
        self.user2 = UserApp.objects.get(username='user2')
        self.user3 = UserApp.objects.get(username='user3')
        self.url = reverse('glossary_rest:progress')
        self.term_pk = 1

    def test_know_before_max(self) -> None:
        """Test the mark as know term, before max value of progress."""
        payload = {'action': 'know', 'id': self.term_pk}

        self.api_client.force_authenticate(self.user2)
        r = self.api_client.post(path=self.url, data=payload, format='json')
        term_progress = Term.objects.get(pk=self.term_pk).progress

        assert term_progress == PROGRESS_MIN + INCREMENT_STEP
        assert r.status_code == status.HTTP_204_NO_CONTENT

    def test_know_on_max(self) -> None:
        """Test the know term, on max value of progress."""
        Term.objects.filter(pk=self.term_pk).update(progress=PROGRESS_MAX)
        payload = {'action': 'know', 'id': self.term_pk}

        self.api_client.force_authenticate(self.user2)
        r = self.api_client.post(path=self.url, data=payload, format='json')
        term_progress = Term.objects.get(pk=self.term_pk).progress

        assert r.status_code == status.HTTP_204_NO_CONTENT
        assert term_progress == PROGRESS_MAX

    def test_not_know_before_min(self) -> None:
        """Test the not know term, before min value of progress."""
        Term.objects.filter(pk=self.term_pk).update(progress=PROGRESS_MAX)
        payload = {'action': 'not_know', 'id': self.term_pk}

        self.api_client.force_authenticate(self.user2)
        r = self.api_client.post(path=self.url, data=payload, format='json')
        term_progress = Term.objects.get(pk=self.term_pk).progress

        assert r.status_code == status.HTTP_204_NO_CONTENT
        assert term_progress == PROGRESS_MAX + DECREMENT_STEP

    def test_not_know_on_min(self) -> None:
        """Test the not know term, on min value of progress."""
        payload = {'action': 'not_know', 'id': self.term_pk}

        self.api_client.force_authenticate(self.user2)
        r = self.api_client.post(path=self.url, data=payload, format='json')
        term_progress = Term.objects.get(pk=self.term_pk).progress

        assert r.status_code == status.HTTP_204_NO_CONTENT
        assert term_progress == PROGRESS_MIN

    def test_forbidden(self) -> None:
        """Test access to term progress for not owner."""
        payload = {'action': 'know', 'id': self.term_pk}

        self.api_client.force_authenticate(self.user3)
        r = self.api_client.post(path=self.url, data=payload, format='json')
        term_progress = Term.objects.get(pk=self.term_pk).progress

        assert r.status_code == status.HTTP_403_FORBIDDEN
        assert term_progress == PROGRESS_MIN
