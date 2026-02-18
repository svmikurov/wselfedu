"""Calculation exercise assignation form."""

from crispy_forms.helper import FormHelper  # type: ignore
from crispy_forms.layout import Button, Div, Layout, Submit  # type: ignore
from django import forms
from django.utils.translation import gettext as _

from apps.users.models import Mentorship

from ..models import AssignedCalculationCondition, CalculationCondition


class MentorshipChoiceField(forms.ModelChoiceField):  # type: ignore
    """Field for student name display of mentorship instance."""

    def label_from_instance(self, obj: Mentorship) -> str:
        """Display student name for mentorship relationship."""
        return str(obj.student)


class AssignCalculationForm(forms.ModelForm):  # type: ignore
    """Assign calculation exercise form."""

    class Meta:
        """Form configuration."""

        model = AssignedCalculationCondition
        fields = ['calculation_condition', 'mentorship']

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        user = kwargs.pop('user')
        form_action = kwargs.pop('form_action')
        super().__init__(*args, **kwargs)  # type: ignore

        self.fields['mentorship'] = MentorshipChoiceField(
            label=_('Student'),
            queryset=Mentorship.objects.filter(mentor=user),  # type: ignore
            required=True,
        )
        self.fields[
            'calculation_condition'
        ].queryset = CalculationCondition.objects.filter(user=user)  # type: ignore
        self.fields['calculation_condition'].label = _('Exercise')

        self.helper = FormHelper()
        self.helper.form_id = 'form'
        self.helper.form_action = form_action

        self.helper.layout = Layout(
            'mentorship',
            'calculation_condition',
            Div(
                Button(
                    'cancel',
                    _('button.cancel'),
                    css_class='wse-btn',
                    onclick=f'document.getElementById({
                        self.helper.form_id!r
                    }).remove()',
                ),
                Submit(
                    'submit',
                    _('button.submit'),
                    css_class='wse-btn',
                    hx_post=self.helper.form_action,
                    hx_target=self.helper.form_id,
                    hx_swap='innerHTML',
                ),
                css_class='d-flex gap-2 justify-content-end',
            ),
        )
