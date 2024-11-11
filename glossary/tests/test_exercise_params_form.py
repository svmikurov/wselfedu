"""Test form of parameters choices for glossary exercise.

Testing:
 * render form with default values;
 * render form with saved values;
 * save user params to database.
"""

from http import HTTPStatus

from django.forms import model_to_dict
from django.test import Client, TestCase
from django.urls import reverse_lazy

from config.constants import (
    DEFAULT_TIMEOUT,
    EDGE_PERIOD_CHOICES,
    EXAMINATION,
    NOT_CHOICES,
    PROGRESS_CHOICES,
    REPEAT,
    STUDY,
    TODAY,
    WEEKS_AGO_2,
    WEEKS_AGO_7,
)
from glossary.models import GlossaryCategory, GlossaryParams, TermSource
from users.models import UserApp

CATEGORY_CHOICES = [
    (0, 'Категория'),
    (1, 'category1-1'),
    (2, 'category1-2'),
    (3, 'category1-3'),
]
"""Category choices to assigned in the form (`list[tuple(int, str)]`).
"""
CATEGORY_INITIAL = 0
"""Category choice alice by default (`int`).
"""
SOURCE_CHOICES = [
    (0, 'Источник'),
    (1, 'source1-1'),
    (2, 'source1-2'),
    (3, 'source1-3'),
]
"""Source choices to assigned in the form (`list[tuple(int, str)]`).
"""
SOURCE_INITIAL = 0
"""Source choice alice by default (`int`).
"""


class ExerciseParamsTest(TestCase):
    """Test the page form with exercise parameters."""

    fixtures = ['users', 'term_category', 'term_source']

    def setUp(self) -> None:
        """Set up the test data."""
        self.client = Client()
        self.url = reverse_lazy('glossary:params')
        self.url_exercise = reverse_lazy('glossary:exercise')

        user_id = 2
        self.user = UserApp.objects.get(pk=user_id)

    def test_status_code_of_render_form(self) -> None:
        """Test the status code of form render."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        assert response.status_code == HTTPStatus.OK

    def test_render_form_with_default_params(self) -> None:
        """Test render the form with default values."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        # Assertions about the values of fields in the rendered form.
        fields = response.context['form'].fields
        assert fields['favorites'].initial is False
        assert fields['category'].choices == CATEGORY_CHOICES
        assert fields['category'].initial == CATEGORY_INITIAL
        assert fields['source'].choices == SOURCE_CHOICES
        assert fields['source'].initial == SOURCE_INITIAL
        assert fields['period_start_date'].choices == EDGE_PERIOD_CHOICES
        assert fields['period_start_date'].initial == NOT_CHOICES
        assert fields['period_end_date'].choices == EDGE_PERIOD_CHOICES[:-1]
        assert fields['period_end_date'].initial == TODAY
        assert fields['progress'].choices == PROGRESS_CHOICES
        assert fields['progress'].initial == [STUDY]
        assert fields['timeout'].initial == DEFAULT_TIMEOUT
        assert fields['save_params'].initial is False

    def test_render_form_with_saved_params(self) -> None:
        """Test render the form with saved params."""
        timeout_value = 7
        category_id = 3
        source_id = 2
        category = GlossaryCategory.objects.get(pk=category_id)
        source = TermSource.objects.get(pk=source_id)

        # Save user params to render.
        GlossaryParams.objects.create(
            user=self.user,
            timeout=timeout_value,
            favorites=True,
            progress=[REPEAT, EXAMINATION],
            period_start_date=WEEKS_AGO_7,
            period_end_date=WEEKS_AGO_2,
            category=category,
            source=source,
        )

        # Request the page with form.
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        # Assertions about the values of fields in the rendered form.
        fields = response.context['form'].fields
        assert fields['favorites'].initial is True
        assert fields['category'].initial == category_id
        assert fields['source'].initial == source_id
        assert fields['period_start_date'].initial == WEEKS_AGO_7
        assert fields['period_end_date'].initial == WEEKS_AGO_2
        assert fields['progress'].initial == [REPEAT, EXAMINATION]
        assert fields['timeout'].initial == timeout_value

    def test_form_to_save_params(self) -> None:
        """Test form to save params."""
        timeout_value = 7
        category_id = 3
        source_id = 2

        # Assertions about the values of fields in the rendered form.
        form = {
            'favorites': True,
            'category': category_id,
            'source': source_id,
            'period_start_date': WEEKS_AGO_7,
            'period_end_date': WEEKS_AGO_2,
            'progress': [REPEAT, EXAMINATION],
            'timeout': timeout_value,
            'save_params': True,
        }

        # Request the page with form.
        self.client.force_login(self.user)
        self.client.post(self.url, data=form)
        params = GlossaryParams.objects.get(user=self.user)

        # Assert that params was saved.
        form.pop('save_params')
        assert form.items() <= model_to_dict(params).items()
