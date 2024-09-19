"""Test glossary api."""

from django.forms.models import model_to_dict
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from glossary.models import GlossaryExerciseParams
from users.models import UserModel


class TestGetGlossaryExerciseParams(APITestCase):
    """Test get Glossary Exercise Params."""

    fixtures = ['tests/tests_drf/fixtures/glossaries.json']

    def setUp(self) -> None:
        """Set up data."""
        self.api_client = APIClient()
        self.user = UserModel.objects.get(username='user1')
        self.url = reverse('api_glossary_exercise_parameters')

    def test_get_glossary_exercise_params(self) -> None:
        """Get glossary exercise params."""
        expect = {
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
                {'alias': 'NC', 'humanly': 'Добавлено'}
            ],
            'categories': [
                {'id': 1,
                 'name': 'GitHub Actions',
                 'url': '',
                 'created_at': '2024-09-07',
                 'user': 1},
                {'id': 2,
                 'name': 'PostgreSQL',
                 'url': '',
                 'created_at': '2024-09-07',
                 'user': 1}
            ],
            'parameters': {
                'period_start_date': 'NC',
                'period_end_date': 'DT',
                'category': 1,
                'progres': 'S'
            },
            'progres': [
                {'alias': 'S', 'humanly': 'Изучаю'},
                {'alias': 'R', 'humanly': 'Повторяю'},
                {'alias': 'E', 'humanly': 'Проверяю'},
                {'alias': 'K', 'humanly': 'Знаю'}
            ]
        }
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expect


class TestUpdateOrCreateGlossaryExerciseParams(APITestCase):
    """Test update or create glossary exersice user default params."""

    fixtures = ['tests/tests_drf/fixtures/glossaries.json']

    def setUp(self) -> None:
        """Set up data."""
        self.api_client = APIClient()
        self.user1 = UserModel.objects.get(username='user1')
        self.user2 = UserModel.objects.get(username='user2')
        self.url = reverse('api_glossary_exercise_parameters')

    def test_update_params(self) -> None:
        """Test update the user exercise specific parameters."""
        request_data = {
            'period_start_date': 'W3',
            'period_end_date': 'W1',
            'category': 1,
            'progres': 'K',
        }
        self.api_client.force_authenticate(user=self.user1)
        response = self.api_client.post(self.url, request_data, format='json')

        user_params = GlossaryExerciseParams.objects.get(user=self.user1)
        user_params = model_to_dict(user_params, fields=request_data)
        assert response.data == user_params
        assert response.data == request_data
        assert response.status_code == status.HTTP_200_OK

    def test_update_params_partially(self) -> None:
        """Test update the user exercise parameters partially."""
        request_data = {
            'period_start_date': 'W2',
            'period_end_date': 'W1',
        }
        expect_data = {
            'period_start_date': 'W2',
            'period_end_date': 'W1',
            'category': 1,
            'progres': 'S',
        }
        self.api_client.force_authenticate(user=self.user1)
        response = self.api_client.post(self.url, request_data, format='json')
        assert response.data == expect_data
        assert response.status_code == status.HTTP_200_OK

    def test_create_default_params(self) -> None:
        """Test create the user exercise default parameters."""
        default_response_data = {
            'period_start_date': 'DT',
            'period_end_date': 'NC',
            'category': None,
            'progres': 'S',
        }
        self.api_client.force_authenticate(user=self.user2)
        response = self.api_client.post(self.url)

        assert response.data == default_response_data
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_specific_default_params(self) -> None:
        """Test create the user exercise specific parameters."""
        request_data = {
            'period_start_date': 'W3',
            'period_end_date': 'W1',
            'category': 1,
            'progres': 'K',
        }
        self.api_client.force_authenticate(user=self.user2)
        response = self.api_client.post(self.url, request_data, format='json')

        user_params = GlossaryExerciseParams.objects.get(user=self.user2)
        user_params = model_to_dict(user_params, fields=request_data)
        assert response.data == user_params
        assert response.data == request_data
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_params_partially(self) -> None:
        """Test create the user exercise parameters partially."""
        request_data = {
            'period_start_date': 'W2',
        }
        expect_data = {
            'period_start_date': 'W2',
            'period_end_date': 'NC',
            'category': None,
            'progres': 'S',
        }
        self.api_client.force_authenticate(user=self.user2)
        response = self.api_client.post(self.url, request_data, format='json')
        assert response.data == expect_data
        assert response.status_code == status.HTTP_201_CREATED
