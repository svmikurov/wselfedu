"""Test Glossary exercise api.

- update progres: increment, decrement, min, max, forbidden,
  TODO: get;
- render task: status, TODO: ...;
- render params: status, create, update, TODO: forbidden;
"""

from unittest import skip

from django.forms.models import model_to_dict
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from config.constants import (
    ANSWER_TEXT,
    ID,
    JSON,
    LEARNED,
    NOT_CHOICES,
    QUESTION_TEXT,
    STUDY,
    TODAY,
    WEEK_AGO,
    WEEKS_AGO_2,
    WEEKS_AGO_3,
)
from glossary.models import GlossaryParams
from users.models import UserApp


class TestGlossaryTask(APITestCase):
    """Test render task data."""

    fixtures = ['glossary/tests/tests_rest/fixtures/glossaries.json']

    def setUp(self) -> None:
        """Set up data."""
        self.api_client = APIClient()
        self.user = UserApp.objects.get(username='user1')
        self.url = reverse('glossary_rest:exercise')

    def test_render_task(self) -> None:
        """Test render exercise."""
        expect = (ID, QUESTION_TEXT, ANSWER_TEXT)
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert tuple(response.json()) == expect


class TestGetGlossaryExerciseParams(APITestCase):
    """Test render Glossary exercise params."""

    fixtures = ['glossary/tests/tests_rest/fixtures/glossaries.json']

    def setUp(self) -> None:
        """Set up data."""
        self.api_client = APIClient()
        self.user = UserApp.objects.get(username='user1')
        self.url = reverse('glossary_rest:params')

    def test_render_glossary_exercise_params(self) -> None:
        """Test render glossary exercise params."""
        expect = {
            'lookup_conditions': {
                'category': 1,
                'period_end_date': 'DT',
                'period_start_date': 'NC',
                'progress': 'S',
            },
            'exercise_choices': {
                'categories': [
                    {
                        'alias': 1,
                        'humanly': 'GitHub Actions',
                    },
                    {
                        'alias': 2,
                        'humanly': 'PostgreSQL',
                    },
                    {
                        'alias': None,
                        'humanly': 'Не выбрано',
                    },
                ],
                'edge_period_items': [
                    {'alias': 'DT', 'humanly': 'Сегодня'},
                    {'alias': 'D3', 'humanly': 'Три дня назад'},
                    {'alias': 'W1', 'humanly': 'Неделя назад'},
                    {'alias': 'W2', 'humanly': 'Две недели назад'},
                    {'alias': 'W3', 'humanly': 'Три недели назад'},
                    {'alias': 'W4', 'humanly': 'Четыре недели назад'},
                    {'alias': 'W7', 'humanly': 'Семь недель назад'},
                    {'alias': 'M3', 'humanly': 'Три месяца назад'},
                    {'alias': 'M6', 'humanly': 'Шесть месяцев назад'},
                    {'alias': 'M9', 'humanly': 'Девять месяцев назад'},
                    {'alias': 'NC', 'humanly': 'Добавлено'},
                ],
                'progress': [
                    {'alias': 'S', 'humanly': 'Изучаю'},
                    {'alias': 'R', 'humanly': 'Повторяю'},
                    {'alias': 'E', 'humanly': 'Проверяю'},
                    {'alias': 'K', 'humanly': 'Знаю'},
                ],
            },
        }
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expect


class TestUpdateOrCreateGlossaryExerciseParams(APITestCase):
    """Test update or create user params for Glossary exersice."""

    fixtures = ['glossary/tests/tests_rest/fixtures/glossaries.json']

    def setUp(self) -> None:
        """Set up data."""
        self.api_client = APIClient()
        self.user1 = UserApp.objects.get(username='user1')
        self.user2 = UserApp.objects.get(username='user2')
        self.url = reverse('glossary_rest:params')

    def test_update_params(self) -> None:
        """Test update the user exercise specific parameters."""
        request_data = {
            'period_start_date': WEEKS_AGO_3,
            'period_end_date': WEEK_AGO,
            'category': 1,
            'progress': LEARNED,
        }
        self.api_client.force_authenticate(user=self.user1)
        response = self.api_client.post(self.url, request_data, format=JSON)

        user_params = GlossaryParams.objects.get(user=self.user1)
        user_params = model_to_dict(user_params, fields=request_data)
        assert response.data == user_params
        assert response.data == request_data
        assert response.status_code == status.HTTP_200_OK

    def test_update_params_partially(self) -> None:
        """Test update the user exercise parameters partially."""
        request_data = {
            'period_start_date': WEEKS_AGO_2,
            'period_end_date': WEEK_AGO,
        }
        expect_data = {
            'period_start_date': WEEKS_AGO_2,
            'period_end_date': WEEK_AGO,
            'category': 1,
            'progress': STUDY,
        }
        self.api_client.force_authenticate(user=self.user1)
        response = self.api_client.post(self.url, request_data, format=JSON)
        assert response.data == expect_data
        assert response.status_code == status.HTTP_200_OK

    # @skip
    def test_create_default_params(self) -> None:
        """Test create the user exercise default parameters."""
        default_response_data = {
            'period_start_date': NOT_CHOICES,
            'period_end_date': TODAY,
            'category': None,
            'progress': STUDY,
        }
        self.api_client.force_authenticate(user=self.user2)
        response = self.api_client.post(self.url)

        assert response.data == default_response_data
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_specific_default_params(self) -> None:
        """Test create the user exercise specific parameters."""
        request_data = {
            'period_start_date': WEEKS_AGO_3,
            'period_end_date': WEEK_AGO,
            'category': 1,
            'progress': LEARNED,
        }
        self.api_client.force_authenticate(user=self.user2)
        response = self.api_client.post(self.url, request_data, format=JSON)

        user_params = GlossaryParams.objects.get(user=self.user2)
        user_params = model_to_dict(user_params, fields=request_data)
        assert response.data == user_params
        assert response.data == request_data
        assert response.status_code == status.HTTP_201_CREATED

    @skip
    def test_create_params_partially(self) -> None:
        """Test create the user exercise parameters partially."""
        request_data = {
            'period_start_date': WEEKS_AGO_2,
        }
        expect_data = {
            'period_start_date': WEEKS_AGO_2,
            'period_end_date': NOT_CHOICES,
            'category': None,
            'progress': STUDY,
        }
        self.api_client.force_authenticate(user=self.user2)
        response = self.api_client.post(self.url, request_data, format=JSON)
        assert response.data == expect_data
        assert response.status_code == status.HTTP_201_CREATED