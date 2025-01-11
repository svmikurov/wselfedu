"""Test Term exercise api.

- update progres: increment, decrement, min, max, forbidden,
  TODO: get;
- render task: status, TODO: ...;
- render params: status, create, update, TODO: forbidden;
"""
from http import HTTPStatus

import pytest
from django.forms.models import model_to_dict
from django.urls import reverse
from rest_framework import status
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.test import APIClient, APITestCase

from config.constants import (
    DEFAULT_SOURCE,
    LEARNED,
    NOT_CHOICES,
    STUDY,
    TODAY,
    WEEK_AGO,
    WEEKS_AGO_2,
    WEEKS_AGO_3,
)
from glossary.models import GlossaryParams
from users.models import UserApp


@pytest.mark.skip
class TestGlossaryTask(APITestCase):
    """Test render task data."""

    fixtures = ['glossary/tests/fixtures/glossaries']

    def setUp(self) -> None:
        """Set up data."""
        self.api_client = APIClient()
        self.user = UserApp.objects.get(username='user1')
        self.url = reverse('glossary_rest:exercise')

    def test_render_task(self) -> None:
        """Test render exercise."""
        expect = ('id', 'question_text', 'answer_text')
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert tuple(response.json()) == expect


@pytest.mark.skip
class TestGetGlossaryExerciseParams(APITestCase):
    """Test render Term exercise params."""

    fixtures = ['glossary/tests/fixtures/glossaries']

    def setUp(self) -> None:
        """Set up data."""
        self.api_client = APIClient()
        self.user = UserApp.objects.get(username='user1')
        self.url = reverse('glossary_rest:params')

    def test_render_glossary_exercise_params(self) -> None:
        """Test render glossary exercise params."""
        expect = {
            'default_values': {
                'timeout': 5,
                'has_timeout': True,
                'favorites': False,
                'progress': ['S'],
                'period_start_date': 'NC',
                'period_end_date': 'DT',
                'is_first': False,
                'is_last': False,
                'count_first': 0,
                'count_last': 0,
                'category': None,
                'source': None
            },
            'lookup_conditions': {
                'category': 1,
                'period_end_date': 'DT',
                'period_start_date': 'NC',
                'progress': [STUDY],
                'timeout': 5,
                'favorites': False,
                'count_first': 0,
                'count_last': 0,
                'source': DEFAULT_SOURCE,
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


@pytest.mark.skip
class TestUpdateOrCreateGlossaryExerciseParams(APITestCase):
    """Test update or create user params for Term exersice."""

    fixtures = ['glossary/tests/fixtures/glossaries']

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
            'progress': [LEARNED],
            'timeout': 5,
            'favorites': False,
            'count_first': 0,
            'count_last': 0,
            'source': DEFAULT_SOURCE,
        }
        self.api_client.force_authenticate(user=self.user1)
        response = self.api_client.put(self.url, request_data, format='json')

        user_params = GlossaryParams.objects.get(user=self.user1)
        user_params = model_to_dict(user_params, fields=request_data)

        assert response.status_code == HTTP_204_NO_CONTENT
        assert user_params == request_data

    def test_create_default_params(self) -> None:
        """Test create the user exercise default parameters."""
        default_response_data = {
            'period_start_date': NOT_CHOICES,
            'period_end_date': TODAY,
            'category': None,
            'progress': [STUDY],
            'timeout': 5,
            'favorites': False,
            'count_first': 0,
            'count_last': 0,
            'source': DEFAULT_SOURCE,
        }
        self.api_client.force_authenticate(user=self.user2)
        response = self.api_client.put(self.url)

        assert response.data == default_response_data
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_specific_default_params(self) -> None:
        """Test create the user exercise specific parameters."""
        request_data = {
            'period_start_date': WEEKS_AGO_3,
            'period_end_date': WEEK_AGO,
            'category': 1,
            'progress': [LEARNED],
            'timeout': 5,
            'favorites': False,
            'count_first': 0,
            'count_last': 0,
            'source': DEFAULT_SOURCE,
        }
        self.api_client.force_authenticate(user=self.user2)
        response = self.api_client.put(self.url, request_data, format='json')

        user_params = GlossaryParams.objects.get(user=self.user2)
        user_params = model_to_dict(user_params, fields=request_data)
        assert response.data == user_params
        assert response.data == request_data
        assert response.status_code == status.HTTP_201_CREATED

    # @skip
    def test_create_params_partially(self) -> None:
        """Test create the user exercise parameters partially."""
        request_data = {
            'period_start_date': WEEKS_AGO_2,
        }
        expect_data = {
            'period_start_date': WEEKS_AGO_2,
            'period_end_date': TODAY,
            'category': None,
            'progress': [STUDY],
            'timeout': 5,
            'favorites': False,
            'count_first': 0,
            'count_last': 0,
            'source': DEFAULT_SOURCE,
        }
        self.api_client.force_authenticate(user=self.user2)
        response = self.api_client.put(self.url, request_data, format='json')
        assert response.data == expect_data
        assert response.status_code == status.HTTP_201_CREATED
