"""Test Create List API views."""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from config.constants import PK
from users.models import UserApp


class TestWordList(APITestCase):
    """Test word list api view."""

    fixtures = ['tests/fixtures/words.json', 'tests/fixtures/users.json']

    def setUp(self) -> None:
        """Set up data."""
        self.api_client = APIClient()
        self.url = reverse('foreign_rest:words')
        self.user1 = UserApp.objects.get(username='user2')
        self.user2 = UserApp.objects.get(username='user3')

    def test_words_permission_for_owner(self) -> None:
        """Test words permission for owner."""
        self.api_client.force_authenticate(user=self.user1)
        response = self.api_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_words_permission_for_anonymous(self) -> None:
        """Test words permission for anonymous."""
        response = self.api_client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_words_permission_for_other_user(self) -> None:
        """Test words permission for other user."""
        self.api_client.force_authenticate(user=self.user2)
        response = self.api_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK


class TestRetrieveWord(APITestCase):
    """Test word list api view."""

    fixtures = ['tests/fixtures/words.json', 'tests/fixtures/users.json']

    def setUp(self) -> None:
        """Set up data."""
        self.api_client = APIClient()
        self.url = reverse('foreign_rest:word', kwargs={PK: 1})
        self.user1 = UserApp.objects.get(username='user2')
        self.user2 = UserApp.objects.get(username='user3')

    def test_word_permission_for_owner(self) -> None:
        """Test word permission for owner."""
        self.api_client.force_authenticate(user=self.user1)
        response = self.api_client.get('/api/v1/foreign/1/')
        assert response.status_code == status.HTTP_200_OK

    def test_word_permission_for_other_user(self) -> None:
        """Test word permission for other user."""
        self.api_client.force_authenticate(user=self.user2)
        response = self.api_client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_word_permission_for_anonymous(self) -> None:
        """Test word permission for anonymous."""
        response = self.api_client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
