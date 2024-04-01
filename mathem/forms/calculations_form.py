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
