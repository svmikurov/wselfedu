"""Test Glossary exercise api.

Test:
    TODO: ...
    - update progres on: increment, decrement, min, max, forbidden,
      TODO: get;
    - render task on: status, TODO: ...;
    - render params on: status, create, update, TODO: forbidden;
"""

from unittest import skip

from django.db.models import Q
from django.forms.models import model_to_dict
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from config.constants import (
    DECREMENT_STEP,
    INCREMENT_STEP,
    PROGRESS_MAX,
    PROGRESS_MIN,
)
from glossary.models import Glossary, GlossaryExerciseParams, GlossaryProgress
from users.models import UserModel


class TestUpdateProgress(APITestCase):
    """Test update Glossary progress."""

    fixtures = ['tests/tests_drf/fixtures/glossaries.json']

    def setUp(self) -> None:
        """Set up data."""
        self.api_client = APIClient()
        self.user1 = UserModel.objects.get(username='user1')
        self.user2 = UserModel.objects.get(username='user2')
        self.url = reverse('api_glossary_term_progress')
        self.term_pk = 1

    def query_term(self, progress: int | None = None) -> GlossaryProgress:
        """Update or create term."""
        obj, _ = GlossaryProgress.objects.update_or_create(
            term=Glossary.objects.get(pk=self.term_pk),
            user=self.user1,
            progress=progress or Q(),
        )
        return obj

    def test_know_before_max(self) -> None:
        """Test mark as know Term before max value."""
        payload = {'action': 'know', 'id': self.term_pk}

        self.api_client.force_authenticate(self.user1)
        r = self.api_client.post(path=self.url, data=payload, format='json')
        term_progress = self.query_term().progress

        assert term_progress == PROGRESS_MIN + INCREMENT_STEP
        assert r.status_code == status.HTTP_200_OK

    def test_know_on_max(self) -> None:
        """Test know term on max value."""
        self.query_term(progress=PROGRESS_MAX)
        payload = {'action': 'know', 'id': self.term_pk}

        self.api_client.force_authenticate(self.user1)
        r = self.api_client.post(path=self.url, data=payload, format='json')
        term_progress = self.query_term().progress

        assert r.status_code == status.HTTP_200_OK
        assert term_progress == PROGRESS_MAX

    def test_not_know_before_min(self) -> None:
        """Test not know term before min value."""
        self.query_term(progress=PROGRESS_MAX)
        payload = {'action': 'not_know', 'id': self.term_pk}

        self.api_client.force_authenticate(self.user1)
        r = self.api_client.post(path=self.url, data=payload, format='json')
        term_progress = self.query_term().progress

        assert r.status_code == status.HTTP_200_OK
        assert term_progress == PROGRESS_MAX + DECREMENT_STEP

    def test_not_know_on_min(self) -> None:
        """Test not know term on min value or has not progress."""
        payload = {'action': 'not_know', 'id': self.term_pk}

        self.api_client.force_authenticate(self.user1)
        r = self.api_client.post(path=self.url, data=payload, format='json')
        term_progress = self.query_term().progress

        assert r.status_code == status.HTTP_200_OK
        assert term_progress == PROGRESS_MIN

    def test_forbidden(self) -> None:
        """Test access to term progress for not owner."""
        payload = {'action': 'know', 'id': self.term_pk}

        self.api_client.force_authenticate(self.user2)
        r = self.api_client.post(path=self.url, data=payload, format='json')

        assert r.status_code == status.HTTP_403_FORBIDDEN
        assert not GlossaryProgress.objects.filter(
            term=Glossary.objects.get(pk=self.term_pk)
        ).exists()


class TestGlossaryTask(APITestCase):
    """Test render task data."""

    fixtures = ['tests/tests_drf/fixtures/glossaries.json']

    def setUp(self) -> None:
        """Set up data."""
        self.api_client = APIClient()
        self.user = UserModel.objects.get(username='user1')
        self.url = reverse('api_glossary_exercise')

    def test_render_task(self) -> None:
        """Test render exercise."""
        expect = ('id', 'question_text', 'answer_text')
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert tuple(response.json()) == expect


class TestGetGlossaryExerciseParams(APITestCase):
    """Test render Glossary exercise params."""

    fixtures = ['tests/tests_drf/fixtures/glossaries.json']

    def setUp(self) -> None:
        """Set up data."""
        self.api_client = APIClient()
        self.user = UserModel.objects.get(username='user1')
        self.url = reverse('api_glossary_exercise_parameters')

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
                        'id': 1,
                        'name': 'GitHub Actions',
                        'url': '',
                        'created_at': '2024-09-07',
                        'user': 1,
                    },
                    {
                        'id': 2,
                        'name': 'PostgreSQL',
                        'url': '',
                        'created_at': '2024-09-07',
                        'user': 1,
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
            'progress': 'K',
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
            'progress': 'S',
        }
        self.api_client.force_authenticate(user=self.user1)
        response = self.api_client.post(self.url, request_data, format='json')
        assert response.data == expect_data
        assert response.status_code == status.HTTP_200_OK

    # @skip
    def test_create_default_params(self) -> None:
        """Test create the user exercise default parameters."""
        default_response_data = {
            'period_start_date': 'NC',
            'period_end_date': 'DT',
            'category': None,
            'progress': 'S',
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
            'progress': 'K',
        }
        self.api_client.force_authenticate(user=self.user2)
        response = self.api_client.post(self.url, request_data, format='json')

        user_params = GlossaryExerciseParams.objects.get(user=self.user2)
        user_params = model_to_dict(user_params, fields=request_data)
        assert response.data == user_params
        assert response.data == request_data
        assert response.status_code == status.HTTP_201_CREATED

    @skip
    def test_create_params_partially(self) -> None:
        """Test create the user exercise parameters partially."""
        request_data = {
            'period_start_date': 'W2',
        }
        expect_data = {
            'period_start_date': 'W2',
            'period_end_date': 'NC',
            'category': None,
            'progress': 'S',
        }
        self.api_client.force_authenticate(user=self.user2)
        response = self.api_client.post(self.url, request_data, format='json')
        assert response.data == expect_data
        assert response.status_code == status.HTTP_201_CREATED
