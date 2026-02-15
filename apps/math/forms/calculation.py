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

from apps.core.forms import UserRelationForm
from apps.core.forms.layouts import create_button_row

from ..models import CalculationCondition, CalculationTypeChoices


class _CalculationConditionsForm(UserRelationForm[CalculationCondition]):
    """Base calculation conditions edit form."""

    FORM_ID = 'form'

    class Meta:
        """Configure the form."""

        model = CalculationCondition
        fields = ['name', 'min_operand', 'max_operand', 'operation_type']

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        super().__init__(*args, **kwargs)

        self.helper.layout = Layout(
            'name',
            Row(Column('min_operand'), Column('max_operand')),
            'operation_type',
            create_button_row(self.helper.form_id),
        )


class CreateCalculationConditionsForm(_CalculationConditionsForm):
    """Base calculation conditions create form."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        super().__init__(*args, **kwargs)
        self.helper.attrs = {
            'hx-post': 'create/',
            'hx-target': f'#{self.FORM_ID}',
            'hx-swap': 'innerHTML',
        }


class UpdateCalculationConditionsForm(_CalculationConditionsForm):
    """Calculation conditions update form."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        super().__init__(*args, **kwargs)
        self.helper.form_action = ''
        self.helper.attrs = {
            'hx-post': reverse(
                'math:regular_calculation_exercise_update',
                kwargs={'pk': self.instance.pk},
            ),
            'hx-target': f'#{self.FORM_ID}',
            'hx-swap': 'innerHTML',
        }


class RegularCalculationConditionsForm(forms.Form):
    """Form for regular calculation conditions select."""

    DEFAULT_OPERAND_MIN_VALUE = 1
    DEFAULT_OPERAND_MAX_VALUE = 9

    calculation_name = forms.CharField(
        max_length=CalculationCondition.MAX_NAME_LENGTH
    )
    min_operand = forms.DecimalField(
        label=_('Min operand value'),
    )
    max_operand = forms.DecimalField(
        label=_('Max operand value'),
    )
    operation_type = forms.ChoiceField(
        choices=CalculationTypeChoices,
        label=_('Operation type'),
    )

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]

        # Form helper with form attributes
        self.helper = FormHelper()
        self.helper.form_id = 'calculation-conditions-form'
        self.helper.form_method = 'get'

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
            Div(
                Submit(
                    '',
                    _('button.exercise.start'),
                    css_class='wse-btn',
                    css_id='button-id-start-exercise',
                    form=self.helper.form_id,
                    formaction=reverse('math:regular_calculation_exercise'),
                ),
                css_class='d-flex gap-2 justify-content-end',
            ),
        )


class NumberInputForm(forms.Form):
    """Form for entering the user's answer in numbers."""

    MAX_DIGITS = 5

    user_answer = forms.DecimalField(
        max_digits=MAX_DIGITS,
        label='',
        widget=forms.NumberInput(
            attrs={
                'autofocus': True,
                'style': 'font-size: 32px; width: 110px',
            }
        ),
    )

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]

        # Form helper with form attributes
        self.helper = FormHelper()
        self.helper.form_id = 'answer-input-form'

        # Form layout
        self.helper.layout = Layout(
            'user_answer',
            Submit(
                'submit',
                _('button.title.answer'),
                css_class='wse-btn',
                hx_post='',
                hx_validate='true',
                hx_swap='innerHTML',
                # HACK: Add target constant for html tag ID
                hx_target='#exercise-block',
            ),
        )
