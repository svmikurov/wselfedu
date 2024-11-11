"""Test form of parameters choices for foreign exercise.

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
    COMBINATION,
    DEFAULT_TIMEOUT,
    DEFAULT_WORD_COUNT,
    EDGE_PERIOD_CHOICES,
    EXAMINATION,
    FROM_NATIVE,
    LANGUAGE_ORDER_CHOICE,
    NOT_CHOICES,
    ONE_WORD,
    PROGRESS_CHOICES,
    REPEAT,
    STUDY,
    TO_NATIVE,
    TODAY,
    WEEKS_AGO_2,
    WEEKS_AGO_7,
    WORD_COUNT_CHOICE,
)
from foreign.models import TranslateParams, WordCategory, WordSource
from users.models import UserApp

CATEGORY_CHOICES = [
    (0, 'Категория'),
    (1, 'category_u3_c1'),
    (2, 'category_u3_c2'),
    (3, 'category_u3_c3'),
    (4, 'category_u3_c4'),
    (5, 'category_u3_c5'),
]
"""Category choices to assigned in the form (`list[tuple(int, str)]`).
"""
CATEGORY_INITIAL = 0
"""Category choice alice by default (`int`).
"""
SOURCE_CHOICES = [
    (0, 'Источник'),
    (1, 'source_u3_s1'),
    (2, 'source_u3_s2'),
    (3, 'source_u3_s3'),
    (4, 'source_u3_s4'),
    (5, 'source_u3_s5'),
]
"""Source choices to assigned in the form (`list[tuple(int, str)]`).
"""
SOURCE_INITIAL = 0
"""Source choice alice by default (`int`).
"""


class ExerciseParamsTest(TestCase):
    """Test the page form with exercise parameters."""

    fixtures = ['users', 'word_category', 'word_source']

    def setUp(self) -> None:
        """Set up the test data."""
        self.client = Client()
        self.url = reverse_lazy('foreign:params')
        self.url_exercise = reverse_lazy('foreign:foreign_translate_demo')

        user_id = 3
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
        assert fields['language_order'].choices == LANGUAGE_ORDER_CHOICE
        assert fields['language_order'].initial == TO_NATIVE
        assert fields['category'].choices == CATEGORY_CHOICES
        assert fields['category'].initial == CATEGORY_INITIAL
        assert fields['source'].choices == SOURCE_CHOICES
        assert fields['source'].initial == SOURCE_INITIAL
        assert fields['period_start_date'].choices == EDGE_PERIOD_CHOICES
        assert fields['period_start_date'].initial == NOT_CHOICES
        assert fields['period_end_date'].choices == EDGE_PERIOD_CHOICES[:-1]
        assert fields['period_end_date'].initial == TODAY
        assert fields['word_count'].choices == WORD_COUNT_CHOICE[1:]
        assert fields['word_count'].initial == DEFAULT_WORD_COUNT
        assert fields['progress'].choices == PROGRESS_CHOICES
        assert fields['progress'].initial == [STUDY]
        assert fields['timeout'].initial == DEFAULT_TIMEOUT
        assert fields['save_params'].initial is False

    def test_render_form_with_saved_params(self) -> None:
        """Test render the form with saved params."""
        timeout_value = 7
        category_id = 3
        source_id = 2
        category = WordCategory.objects.get(pk=category_id)
        source = WordSource.objects.get(pk=source_id)

        # Save user params to render.
        TranslateParams.objects.create(
            user=self.user,
            timeout=timeout_value,
            favorites=True,
            progress=[REPEAT, EXAMINATION],
            period_start_date=WEEKS_AGO_7,
            period_end_date=WEEKS_AGO_2,
            language_order=FROM_NATIVE,
            category=category,
            source=source,
            word_count=[ONE_WORD, COMBINATION],
        )

        # Request the page with form.
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        # Assertions about the values of fields in the rendered form.
        fields = response.context['form'].fields
        assert fields['favorites'].initial is True
        assert fields['language_order'].initial == FROM_NATIVE
        assert fields['category'].initial == category_id
        assert fields['source'].initial == source_id
        assert fields['period_start_date'].initial == WEEKS_AGO_7
        assert fields['period_end_date'].initial == WEEKS_AGO_2
        assert fields['word_count'].initial == [ONE_WORD, COMBINATION]
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
            'language_order': FROM_NATIVE,
            'category': category_id,
            'source': source_id,
            'period_start_date': WEEKS_AGO_7,
            'period_end_date': WEEKS_AGO_2,
            'word_count': [ONE_WORD, COMBINATION],
            'progress': [REPEAT, EXAMINATION],
            'timeout': timeout_value,
            'save_params': True,
        }

        # Request the page with form.
        self.client.force_login(self.user)
        self.client.post(self.url, data=form)
        params = TranslateParams.objects.get(user=self.user)

        # Assert that params was saved.
        form.pop('save_params')
        assert form.items() <= model_to_dict(params).items()
