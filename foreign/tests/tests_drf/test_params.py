"""Translate word exercise user parameters."""

from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.test import APIClient, APITestCase

from config.constants import LEARNED, STUDY, WEEK_AGO, WEEKS_AGO_3
from foreign.models import WordCategory
from users.models import UserApp


class RenderParamsTest(APITestCase):
    """Render translate foreign words exercise the user params test."""

    fixtures = ['tests/fixtures/users.json', 'tests/fixtures/foreign.json']

    def setUp(self) -> None:
        """Set up test data."""
        self.api_client = APIClient()
        self.url = reverse('rest_foreign:params')
        self.user = UserApp.objects.get(pk=3)

    def test_get_request(self) -> None:
        """Test the GET request method."""
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.get(self.url)
        payload = response.json()

        assert response.status_code == HTTP_200_OK
        assert list(payload) == ['lookup_conditions', 'exercise_choices']
        assert list(payload['exercise_choices']) == [
            'edge_period_items', 'categories', 'progress'
        ]  # fmt: skip

    def test_post_request(self) -> None:
        """Test the POST request method."""
        # Create category instants
        cat_pk = WordCategory.objects.create(name='cat', user=self.user).pk

        self.api_client.force_authenticate(user=self.user)
        payload = {
            'period_start_date': WEEKS_AGO_3,
            'period_end_date': WEEK_AGO,
            'category': cat_pk,
            'progress': LEARNED,
        }
        response = self.api_client.post(self.url, data=payload, format='json')

        assert response.status_code == HTTP_201_CREATED

    def test_post_request_empty_payload(self) -> None:
        """Test the POST request method without payload."""
        self.api_client.force_authenticate(user=self.user)
        payload = {}
        response = self.api_client.post(self.url, data=payload, format='json')
        # Adda default params
        assert response.status_code == HTTP_201_CREATED

    def test_post_request_validation_error(self) -> None:
        """Test the POST request with data validation error."""
        self.api_client.force_authenticate(user=self.user)
        payload = {'category': 'value'}
        response = self.api_client.post(self.url, data=payload, format='json')
        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_post_request_array_field(self) -> None:
        """Test the POST request with data validation error."""
        self.api_client.force_authenticate(user=self.user)
        # Will raise an assertion error after adding a field to the
        # serializer.
        payload = {'word_count': STUDY}
        response = self.api_client.post(self.url, data=payload, format='json')
        assert response.status_code == HTTP_201_CREATED

    def test_rename_model_field(self) -> None:
        """Test the render category field names."""
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.get(self.url)
        fields = response.json()['exercise_choices']['categories'].pop().keys()
        assert ['alias', 'humanly'] == list(fields)

    def test_add_no_selection(self) -> None:
        """Test the add no selection to category list."""
        self.api_client.force_authenticate(self.user)
        response = self.api_client.get(self.url)
        categories = response.json()['exercise_choices']['categories']
        no_selection = {
            'alias': None,
            'humanly': 'Не выбрано',
        }
        assert no_selection in categories
