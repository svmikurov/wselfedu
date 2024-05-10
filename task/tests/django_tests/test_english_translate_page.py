import pytest
from django.test import TestCase
from django.urls import reverse_lazy

from contrib_app.contrib_test import TestMixin


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

    @pytest.mark.filterwarnings("ignore")
    def test_page_get_status_redirect(self):
        """Test get method redirect status for invalid task conditions."""
        msg = 'Не задан таймаут или порядок перевода слов'
        response = self.get_user_auth_response()
        self.flash_message_test(response, msg)
        self.assertEqual(response.status_code, 302)
