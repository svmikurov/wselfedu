"""Calculate exercise conditions choice form."""

from typing import Any

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Field, Layout, Row, Submit
from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError

from config.constants import (
    BTN_SM,
    CALCULATION_TYPES,
    SUBMIT,
    W_25,
    W_50,
)


class CalculationChoiceForm(forms.Form):
    """Form for choosing the conditions of a mathematical task."""

    DEFAULT_TIMEOUT = 2
    DEFAULT_CALCULATION_TYPE_INDEX = 2
    DEFAULT_MIN_VALUE = 2
    DEFAULT_MAX_VALUE = 9

    exercise = forms.ChoiceField(
        choices=CALCULATION_TYPES,
        initial=CALCULATION_TYPES[DEFAULT_CALCULATION_TYPE_INDEX],
        label='Вид вычисления',
    )
    min_value = forms.IntegerField(
        initial=DEFAULT_MIN_VALUE,
        label='Минимальное число',
    )
    max_value = forms.IntegerField(
        initial=DEFAULT_MAX_VALUE,
        label='Максимальное число',
    )
    timeout = forms.IntegerField(
        initial=DEFAULT_TIMEOUT,
        label='Время на ответ (сек)',
    )
    with_solution = forms.BooleanField(
        required=False,
        label='С вводом ответа',
    )

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Add attribute ``request`` for rendering messages at page."""
        self.request = kwargs.pop('request')
        super(CalculationChoiceForm, self).__init__(*args, **kwargs)

    def clean(self) -> dict[str, Any]:
        """Validate the entered by form task conditions."""
        cleaned_data = super().clean()
        min_value = cleaned_data.get('min_value')
        max_value = cleaned_data.get('max_value')
        timeout = cleaned_data.get('timeout')

        if min_value is not None:
            if min_value >= max_value:
                msg = (
                    'Минимальное число должно быть '
                    'меньше максимального числа'
                )
                messages.error(self.request, msg)
                raise ValidationError('min_value must be less than max_value')

            if min_value < 1 or max_value < 1 or timeout < 1:
                msg = 'Число должно натуральным'
                messages.error(self.request, msg)
                raise ValidationError('The number must be natural')

        return cleaned_data

    @property
    def helper(self) -> FormHelper:
        """Django-crispy-form helper."""
        helper = FormHelper()
        helper.form_method = 'GET'
        helper.form_id = 'math_calculate_choice'

        helper.layout = Layout(
            Row(
                Column(
                    Field(
                        'exercise',
                        css_class=W_50,
                        data_testid='calculation_type',
                    ),
                ),
                Column(
                    Field('timeout', css_class=W_25),
                ),
            ),
            Row(
                Column(
                    Field('min_value', css_class=W_25),
                ),
                Column(
                    Field('max_value', css_class=W_25),
                ),
            ),
            Field('with_solution'),
            Submit(SUBMIT, 'Начать', css_class=BTN_SM),
        )

        return helper
