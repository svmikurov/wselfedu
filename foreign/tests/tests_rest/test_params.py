"""Translate word exercise user parameters."""

from django.forms import model_to_dict
from django.urls import reverse
from rest_framework import status
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.test import APIClient, APITestCase

from config.constants import (
    LEARNED,
    STUDY,
    WEEK_AGO,
    WEEKS_AGO_3,
)
from foreign.models import TranslateParams, WordCategory
from users.models import UserApp


class RenderParamsTest(APITestCase):
    """Render translate foreign words exercise the user params test."""

    fixtures = ['tests/fixtures/users.json', 'tests/fixtures/foreign.json']

    def setUp(self) -> None:
        """Set up test data."""
        self.api_client = APIClient()
        self.url = reverse('foreign_rest:params')
        self.user = UserApp.objects.get(pk=3)

    def test_get_params(self) -> None:
        """Test request to get params."""
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.get(self.url)
        payload = response.json()

        assert response.status_code == HTTP_200_OK
        assert list(payload) == ['lookup_conditions', 'exercise_choices']
        assert list(payload['exercise_choices']) == [
            'edge_period_items', 'categories', 'progress'
        ]  # fmt: skip

    def test_save_params(self) -> None:
        """Test request to save params."""
        cat_pk = WordCategory.objects.create(name='cat', user=self.user).pk
        self.api_client.force_authenticate(user=self.user)
        payload = {
            'period_start_date': WEEKS_AGO_3,
            'period_end_date': WEEK_AGO,
            'category': cat_pk,
            'progress': LEARNED,
            'count_first': 33,
            'count_last': 77,
        }
        response = self.api_client.put(self.url, data=payload, format='json')
        queryset = TranslateParams.objects.get(user=self.user)

        assert response.status_code == status.HTTP_201_CREATED
        assert payload.items() <= model_to_dict(queryset).items()

    def test_put_request_empty_payload(self) -> None:
        """Test the POST request method without payload."""
        self.api_client.force_authenticate(user=self.user)
        payload = {}
        response = self.api_client.put(self.url, data=payload, format='json')
        # Adds default params
        assert response.status_code == status.HTTP_201_CREATED

    def test_put_request_validation_error(self) -> None:
        """Test the POST request with data validation error."""
        self.api_client.force_authenticate(user=self.user)
        payload = {'category': 'value'}
        response = self.api_client.put(self.url, data=payload, format='json')
        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_put_request_array_field(self) -> None:
        """Test the PUT request with data validation error."""
        self.api_client.force_authenticate(user=self.user)
        # Will raise an assertion error after adding a field to the
        # serializer.
        payload = {'word_count': STUDY}
        response = self.api_client.put(self.url, data=payload, format='json')
        assert response.status_code == status.HTTP_201_CREATED

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
