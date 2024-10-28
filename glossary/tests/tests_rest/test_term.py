"""Glossary term REST endpoints tests."""

from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.test import APIClient, APITestCase

from users.models import UserApp


class GlossaryListTest(APITestCase):
    """Glossary term list REST endpoint tests."""

    fixtures = ['users.json', 'terms.json']

    def setUp(self) -> None:
        """Set up data."""
        self.api_client = APIClient()
        self.url = reverse('glossary_rest:terms')
        self.user2 = UserApp.objects.get(pk=2)
        self.user3 = UserApp.objects.get(pk=3)

    def test_permissions_anonymous(self) -> None:
        """Test the glossary list permissions for anonymous."""
        response = self.api_client.get(self.url)
        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_permissions_auth(self) -> None:
        """Test the glossary list permissions for auth user."""
        self.api_client.force_authenticate(self.user2)
        response = self.api_client.get(self.url)
        assert response.status_code == HTTP_200_OK

    def test_permissions_owner(self) -> None:
        """Test the glossary list permissions for owner."""
        self.api_client.force_authenticate(self.user3)
        terms = self.api_client.get(self.url).json()['results']
        assert [term['term'] for term in terms] == [
            'term3-1',
            'term3-2',
            'term3-3',
        ]


class GlossaryCreateTest(APITestCase):
    """Create Glossary term REST endpoint tests."""

    fixtures = ['users.json']

    def setUp(self) -> None:
        """Set up data."""
        self.api_client = APIClient()
        self.url = reverse('glossary_rest:terms')
        self.user2 = UserApp.objects.get(pk=2)
        self.term = {
            'term': 'term',
            'definition': 'definition',
        }

    def test_create_by_anonymous(self) -> None:
        """Test the create term permission for anonymous."""
        response = self.api_client.post(self.url, self.term)
        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_create_by_auth_user(self) -> None:
        """Test the create term permission for auth user."""
        self.api_client.force_authenticate(self.user2)
        response = self.api_client.post(self.url, self.term, format='json')
        assert response.status_code == HTTP_201_CREATED
