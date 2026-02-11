"""Calculate exercise form input module."""

from crispy_forms.helper import FormHelper  # type: ignore[import-untyped]
from crispy_forms.layout import (  # type: ignore[import-untyped]
    Column,
    Div,
    Layout,
    Row,
    Submit,
)
from django import forms
from django.urls import reverse
from django.utils.translation import gettext as _

from apps.core.forms.layouts import create_submit_button

from ..models import ExerciseCondition


class CalculationConditionsForm(forms.Form):
    """Form for calculation conditions select."""

    DEFAULT_OPERAND_MIN_VALUE = 1
    DEFAULT_OPERAND_MAX_VALUE = 9

    calculation_name = forms.CharField(
        max_length=ExerciseCondition.MAX_NAME_LENGTH
    )
    min_operand = forms.DecimalField(
        label=_('Min operand value'),
    )
    max_operand = forms.DecimalField(
        label=_('Max operand value'),
    )
    operation_type = forms.ChoiceField(
        choices=[
            ('add', _('Adding')),
            ('sub', _('Submission')),
            ('mul', _('Multiplication')),
            ('div', _('Division')),
        ],
        label=_('Operation type'),
    )

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]

        # Form helper with form attributes
        self.helper = FormHelper()
        self.helper.form_id = 'calculation-conditions-form'

        # Initial form values
        self.fields['min_operand'].initial = self.DEFAULT_OPERAND_MIN_VALUE
        self.fields['max_operand'].initial = self.DEFAULT_OPERAND_MAX_VALUE

        # Form layout
        self.helper.layout = Layout(
            Row(
                Column('min_operand'),
                Column('max_operand'),
                Column('operation_type'),
                css_class='align-items-end',
            ),
            # Buttons row
            Div(
                # Start exercise with form data conditions button
                Submit(
                    'calculation_conditions',
                    _('button.exercise.start'),
                    css_class='wse-btn',
                    form=self.helper.form_id,
                    formaction=reverse('math:regular_calculation_exercise'),
                    formmethod='GET',
                ),
                # Save form data exercise conditions button
                create_submit_button(),
                # Buttons row style
                css_class='d-flex gap-2 justify-content-end',
            ),
        )


class NumberInputForm(forms.Form):
    """Form for entering the user's answer in numbers."""

    MAX_DIGITS = 5

    user_solution = forms.DecimalField(
        max_digits=MAX_DIGITS,
        label='',
        widget=forms.NumberInput(
            attrs={
                'autofocus': True,
                'style': 'font-size: 32px; width: 110px',
            }
        ),
    )
