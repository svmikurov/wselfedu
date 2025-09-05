"""Defines integration tests for IndexViewSet."""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import Balance

User = get_user_model()


class IndexViewSetIntegrationTest(APITestCase):
    """Integration tests for IndexViewSet."""

    def setUp(self) -> None:
        """Set up test data."""
        self.url = reverse('core:core_index-index')
        self.user_data = {
            'username': 'test_user',
            'password': 'test_pass123',
        }
        self.user = User.objects.create_user(**self.user_data)
        self.balance = Balance.objects.create(user=self.user, total=100)

    def test_index_unauthenticated(self) -> None:
        """Test index endpoint with unauthenticated request."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance'], None)
        self.assertIs(response.data['balance'], None)

    def test_index_authenticated(self) -> None:
        """Test index endpoint with authenticated user."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('balance', response.data)
        self.assertEqual(response.data['balance'], '100')
