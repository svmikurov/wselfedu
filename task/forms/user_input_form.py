from django import forms


class NumberInputForm(forms.Form):
    """Form for entering the user's answer in numbers."""

    MAX_DIGITS = 5

    user_solution = forms.DecimalField(
        max_digits=MAX_DIGITS,
        label='',
        widget=forms.NumberInput(attrs={
            'autofocus': True,
            'style': 'font-size: 32px; width: 110px',
        }),
    )
