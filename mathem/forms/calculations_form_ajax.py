from django import forms


class CalculationAjaxForm(forms.Form):
    """Calculations task ajax form."""

    MAX_ANSWER_DIGITS = 3

    user_answer = forms.DecimalField(
        max_digits=MAX_ANSWER_DIGITS,
        required=False,
    )
