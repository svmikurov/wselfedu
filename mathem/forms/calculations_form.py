from django import forms

CALCULATION_TYPES = (
    ('ADD', 'Сложение'),
    ('SUB', 'Вычитание'),
    ('MUL', 'Умножение'),
)


class CalculationsForms(forms.Form):
    calculation_type = forms.ChoiceField(
        choices=CALCULATION_TYPES,
    )
    question_field = forms.CharField(
        max_length=20,
    )


class CalculationChoiceForm(forms.Form):
    """Calculations task form."""

    CALCULATION_TYPES = (
        ('ADD', 'Сложение'),
        ('SUB', 'Вычитание'),
        ('MUL', 'Умножение'),
        # ('CHS', 'Выберите вычисление')
    )
    DEFAULT_CALCULATION_TYPES = ('MUL', 'Умножение')
    MIN_INITIAL_NUMBER = 1
    MAX_INITIAL_NUMBER = 10
    MAX_DIGITS = 5
    MAX_ANSWER_DIGITS = 3

    calculation_type = forms.ChoiceField(
        choices=CALCULATION_TYPES,
        initial=DEFAULT_CALCULATION_TYPES,
    )
    min_value = forms.DecimalField(
        max_digits=MAX_DIGITS,
        initial=MIN_INITIAL_NUMBER,
    )
    max_value = forms.DecimalField(
        max_digits=MAX_DIGITS,
        initial=MAX_INITIAL_NUMBER,
    )
    question_field = forms.CharField(
        max_length=20,
        required=False,
    )
    user_answer_form = forms.DecimalField(
        max_digits=MAX_DIGITS,
        required=False,
    )
