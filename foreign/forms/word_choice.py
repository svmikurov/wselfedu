"""Foreign translate conditions choice module."""

from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Field, Layout, Row, Submit
from django import forms
from django.db import models

from config.constants import (
    BTN_SM,
    CATEGORY,
    COL_6,
    DEFAULT_CREATE_CHOICE_VALUE,
    DEFAULT_LANGUAGE_ORDER,
    DEFAULT_PROGRESS,
    DEFAULT_TIMEOUT,
    DEFAULT_WORD_COUNT,
    EDGE_PERIOD_CHOICES,
    FAVORITES,
    LANGUAGE_ORDER,
    LANGUAGE_ORDER_CHOICE,
    NOT_CHOICES,
    PERIOD_END_DATE,
    PERIOD_START_DATE,
    POST,
    PROGRESS,
    PROGRESS_CHOICES,
    SOURCE,
    SUBMIT,
    TIMEOUT,
    TODAY,
    WORD_COUNT,
    WORD_COUNT_CHOICE,
)
from foreign.models import WordCategory, WordSource


class ForeignTranslateChoiceForm(forms.Form):
    """Foreign word translation conditions choice form."""

    MODEL_FIELDS = {
        CATEGORY: WordCategory,
        SOURCE: WordSource,
    }

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Init user's model instances at form fields."""
        user_id = kwargs.pop('request').user.id
        super(ForeignTranslateChoiceForm, self).__init__(*args, **kwargs)
        for field, model in self.MODEL_FIELDS.items():
            self.fields[field].choices = self._create_choices(model, user_id)

    favorites = forms.BooleanField(
        required=False,
    )
    language_order = forms.ChoiceField(
        choices=LANGUAGE_ORDER_CHOICE,
        initial=DEFAULT_LANGUAGE_ORDER,
        required=False,
        label='',
    )
    category = forms.TypedChoiceField(
        initial=DEFAULT_CREATE_CHOICE_VALUE,
        required=False,
        label='',
    )
    source = forms.TypedChoiceField(
        initial=DEFAULT_CREATE_CHOICE_VALUE,
        required=False,
        label='',
    )
    period_start_date = forms.ChoiceField(
        choices=EDGE_PERIOD_CHOICES,
        initial=NOT_CHOICES,
        required=False,
        label='',
    )
    period_end_date = forms.ChoiceField(
        choices=EDGE_PERIOD_CHOICES[:-1],
        initial=TODAY,
        required=False,
        label='',
    )
    word_count = forms.MultipleChoiceField(
        choices=WORD_COUNT_CHOICE[1:],
        initial=DEFAULT_WORD_COUNT,
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label='Слово, длина выражения',
    )
    progress = forms.MultipleChoiceField(
        choices=PROGRESS_CHOICES,
        initial=DEFAULT_PROGRESS,
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label='Этап изучения слов',
    )
    timeout = forms.IntegerField(
        initial=DEFAULT_TIMEOUT,
        label='Время на ответ (сек)',
    )

    def clean(self) -> dict[str, int]:
        """Convert `str` to `int` form values."""
        cleaned_data = super().clean()
        cleaned_data[CATEGORY] = self._to_int(cleaned_data, CATEGORY)
        cleaned_data[SOURCE] = self._to_int(cleaned_data, SOURCE)
        return cleaned_data

    @staticmethod
    def _to_int(cleaned_data: dict[str, str], field_name: str) -> int:
        """Convert `str` to `int` field value."""
        field_value = cleaned_data.get(field_name)
        return int(field_value) if field_value else field_value

    @staticmethod
    def _create_choices(
        model: models.Model,
        user_id: id,
    ) -> list[tuple[int, str]]:
        """Create human-readable choice by model and user_id."""
        model_name = model._meta.verbose_name
        default_choice = (DEFAULT_CREATE_CHOICE_VALUE, model_name)
        choices = [default_choice]

        # Populate a list of choices.
        queryset = model.objects.filter(user_id=user_id)
        for instance in queryset:
            model_value, human_readable_name = instance.pk, str(instance)
            choice = (model_value, human_readable_name)
            choices.append(choice)

        return choices

    @property
    def helper(self) -> FormHelper:
        """Structure the form."""
        helper = FormHelper()
        helper.form_method = POST

        helper.layout = Layout(
            Row(
                Column(
                    FAVORITES,
                    css_class=COL_6,
                    data_testid=FAVORITES,
                ),
                Column(
                    LANGUAGE_ORDER,
                    css_class=COL_6,
                    data_testid=LANGUAGE_ORDER,
                ),
            ),
            Row(
                Column(CATEGORY, css_class=COL_6),
                Column(SOURCE, css_class=COL_6),
            ),
            Row(
                HTML('<label class="h6">Период добавления слова</label>'),
                Column(PERIOD_START_DATE, css_class=COL_6),
                Column(PERIOD_END_DATE, css_class=COL_6),
                data_testid='word_addition_period',
            ),
            InlineCheckboxes(PROGRESS, data_testid=PROGRESS),
            Submit(SUBMIT, 'Начать', css_class=BTN_SM, data_testid=SUBMIT),
            HTML('<p class="h6 pt-3">Дополнительные опции</p>'),
            Field(TIMEOUT, css_class='form-group col-6 w-25'),
            InlineCheckboxes(WORD_COUNT, data_testid=WORD_COUNT),
        )

        return helper
