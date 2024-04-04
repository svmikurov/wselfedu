from django import forms

CALCULATION_TYPES = (
    ('ADD', 'Сложение'),
    ('SUB', 'Вычитание'),
    ('MUL', 'Умножение'),
)


class MathTaskChoiceForm(forms.Form):
    """Math task choice  form."""

    CALCULATION_TYPES = (
        ('+', 'Сложение'),
        ('-', 'Вычитание'),
        ('*', 'Умножение'),
        # ('CHS', 'Выберите вычисление')
    )
    DEFAULT_CALCULATION_TYPES_INDEX = 0
    MIN_INITIAL_NUMBER = 1
    MAX_INITIAL_NUMBER = 10
    MAX_DIGITS = 5

    calculation_type = forms.ChoiceField(
        choices=CALCULATION_TYPES,
        initial=CALCULATION_TYPES[DEFAULT_CALCULATION_TYPES_INDEX],
    )
    min_value = forms.DecimalField(
        max_digits=MAX_DIGITS,
        initial=MIN_INITIAL_NUMBER,
    )
    max_value = forms.DecimalField(
        max_digits=MAX_DIGITS,
        initial=MAX_INITIAL_NUMBER,
    )
