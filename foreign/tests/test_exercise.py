"""Test the foreign word translate page."""

from unittest import skip

import pytest
from django.urls import reverse_lazy

from config.constants import (
    TO_NATIVE,
)
from contrib.tests.extension import UserAuthTestCase


@pytest.mark.skip
class TestAuthForeignTranslateExercisePage(UserAuthTestCase):
    """Foreign word translate exercise test."""

    fixtures = ['tests/fixtures/foreign.json', 'tests/fixtures/users.json']

    user_id = 3
    url = reverse_lazy('foreign:foreign_translate_demo')

    @pytest.mark.filterwarnings('ignore')
    # https://docs.pytest.org/en/stable/how-to/capture-warnings.html#pytest-mark-filterwarnings
    def test_page_get_status_success(self) -> None:
        """Test get method success status."""
        task_conditions = {'timeout': 1, 'order': TO_NATIVE}
        self.set_session(**{'task_conditions': task_conditions})
        response = self.get_auth_response()
        self.assertEqual(response.status_code, 200)

    @pytest.mark.filterwarnings('ignore')
    def test_page_get_status_invalid_task_conditions(self) -> None:
        """Test redirect status for invalid task conditions."""
        msg = 'Не задан таймаут или порядок перевода слов'
        response = self.get_auth_response()
        self.assertMessage(response, msg)
        self.assertEqual(response.status_code, 302)

    def test_page_get_status_redirect_anonymous(self) -> None:
        """Test get method redirect status anonymous."""
        msg = 'Для доступа необходимо войти в приложение'
        expected_url = reverse_lazy('users:login')
        response = self.client.get(self.url)
        self.assertRedirects(response, expected_url, 302)
        self.assertMessage(response, msg)
