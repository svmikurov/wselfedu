from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, Submit
from django import forms


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
        label='Максимальное число'
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

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = 'GET'
        helper.form_id = 'select_math_conditions'

        helper.layout = Layout(
            Row(
                Column(
                    Field('calculation_type', css_class="w-50"),
                ),
                Column(
                    Field('timeout', css_class="w-25"),
                )
            ),
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
