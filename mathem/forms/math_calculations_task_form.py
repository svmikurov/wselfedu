from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, Submit
from django import forms
from django.contrib import messages
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
    min_value = forms.IntegerField(
        initial=MIN_INITIAL_VALUE,
        label='Минимальное число',
        widget=forms.NumberInput(attrs={'class': "w-25"})
    )
    max_value = forms.IntegerField(
        initial=MAX_INITIAL_VALUE,
        label='Максимальное число',
    )
    timeout = forms.IntegerField(
        initial=INITIAL_TIMEOUT,
        label='Время на ответ (сек)',
    )
    with_solution = forms.BooleanField(
        required=False,
        label='С вводом ответа',
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(MathTaskCommonSelectForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        min_value = cleaned_data.get('min_value')
        max_value = cleaned_data.get('max_value')
        timeout = cleaned_data.get('timeout')
        print(f'min_value = {min_value}')

        if min_value and max_value and min_value >= max_value:
            msg = 'Минимальное число должно быть меньше максимального числа'
            messages.error(self.request, msg)
            raise ValidationError('min_value must be less than max_value')

        if min_value is not None:
            if min_value < 1 or max_value < 1 or timeout < 1:
                msg = 'Число должно натуральным'
                messages.error(self.request, msg)
                raise ValidationError('The number must be natural')

        return cleaned_data

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
