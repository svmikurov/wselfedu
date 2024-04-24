from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, Submit
from django import forms
from django.forms import NumberInput


class MathTaskCommonSelectForm(forms.Form):
    """Form for choosing the conditions of a mathematical task."""

    CALCULATION_TYPES = (
        ('+', 'Сложение'),
        ('-', 'Вычитание'),
        ('*', 'Умножение'),
    )
    DEFAULT_CALCULATION_TYPES_INDEX = 2
    MIN_INITIAL_VALUE = 2
    MAX_INITIAL_VALUE = 9
    MAX_DIGITS = 5

    calculation_type = forms.ChoiceField(
        choices=CALCULATION_TYPES,
        initial=CALCULATION_TYPES[DEFAULT_CALCULATION_TYPES_INDEX],
        label='Выберите тип вычислений',
    )
    min_value = forms.DecimalField(
        max_digits=MAX_DIGITS,
        initial=MIN_INITIAL_VALUE,
        label='Минимальное значение числа',
        widget=NumberInput(attrs={'class': "w-25"})
    )
    max_value = forms.DecimalField(
        max_digits=MAX_DIGITS,
        initial=MAX_INITIAL_VALUE,
        label='Максимальное значение числа'
    )

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
            Submit('Submit', 'Начать'),
        )

        return helper
