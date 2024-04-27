from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, Submit
from django import forms
from django.core.exceptions import ValidationError


class MathTaskCommonSelectForm(forms.Form):
    """Form for choosing the conditions of a mathematical task."""

    CALCULATION_TYPES = (
        ('+', 'Сложение'),
        ('-', 'Вычитание'),
        ('*', 'Умножение'),
    )
    INITIAL_TIMEOUT = 2
    DEFAULT_CALCULATION_TYPES_INDEX = 2
    MIN_INITIAL_VALUE = 2
    MAX_INITIAL_VALUE = 9
    MAX_DIGITS = 5

    calculation_type = forms.ChoiceField(
        choices=CALCULATION_TYPES,
        initial=CALCULATION_TYPES[DEFAULT_CALCULATION_TYPES_INDEX],
        label='Вид вычисления',
    )
    min_value = forms.DecimalField(
        max_digits=MAX_DIGITS,
        initial=MIN_INITIAL_VALUE,
        label='Минимальное число',
        widget=forms.NumberInput(attrs={'class': "w-25"})
    )
    max_value = forms.DecimalField(
        max_digits=MAX_DIGITS,
        initial=MAX_INITIAL_VALUE,
        label='Максимальное число',
    )
    timeout = forms.DecimalField(
        max_digits=2,
        initial=INITIAL_TIMEOUT,
        label='Время на ответ (сек)',
    )
    with_solution = forms.BooleanField(
        required=False,
        label='С вводом ответа',
    )

    def clean(self):
        cleaned_data = super().clean()
        min_value = cleaned_data.get('min_value')
        max_value = cleaned_data.get('max_value')

        if min_value and max_value and min_value >= max_value:
            raise ValidationError('min_value must be less than max_value')

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = 'GET'
        helper.form_id = 'select_math_conditions'

        helper.layout = Layout(
            Field('calculation_type', css_class="w-50"),
            Row(
                Column(
                    Field('min_value', css_class=""),
                ),
                Column(
                    Field('max_value', css_class="w-25"),
                ),
            ),
            Field('with_solution'),
            Submit('Submit', 'Начать', css_class='btn-sm'),
        )

        return helper
