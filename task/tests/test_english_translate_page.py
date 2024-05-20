from unittest import skip

import pytest
from django.test import TestCase
from django.urls import reverse_lazy

from contrib.mixins_tests import TestMixin


class TestEnglishTranslateChoicePage(TestMixin, TestCase):
    """English word translate condition choice test."""


class TestEnglishTranslateExercisePage(TestMixin, TestCase):
    """English word translate exercise test."""

    fixtures = ['task/tests/fixtures/wse-fixtures-4.json']

    user_id = 3
    url = reverse_lazy('task:english_translate_demo')

    @pytest.mark.filterwarnings("ignore")
    # https://docs.pytest.org/en/stable/how-to/capture-warnings.html#pytest-mark-filterwarnings
    def test_page_get_status_success(self):
        """Test get method success status."""
        task_conditions = {'timeout': 1, 'language_order': 'EN'}
        self.set_session(**{'task_conditions': task_conditions})
        response = self.get_user_auth_response()
        self.assertEqual(response.status_code, 200)

    @skip
    @pytest.mark.filterwarnings("ignore")
    def test_page_get_status_invalid_task_conditions(self):
        """Test get method redirect status for invalid task conditions."""
        msg = 'Не задан таймаут или порядок перевода слов'
        response = self.get_user_auth_response()
        self.assertMessage(response, msg)
        self.assertEqual(response.status_code, 302)

    def test_page_get_status_redirect_anonymous(self):
        """Test get method redirect status anonymous."""
        msg = 'Для доступа необходимо войти в приложение'
        expected_url = reverse_lazy('users:login')
        response = self.client.get(self.url)
        self.assertRedirects(response, expected_url, 302)
        self.assertMessage(response, msg)
