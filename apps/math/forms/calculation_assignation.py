"""Calculation exercise assignation form."""

from crispy_forms.helper import FormHelper  # type: ignore
from crispy_forms.layout import (  # type: ignore
    Button,
    Column,
    Div,
    Layout,
    Row,
    Submit,
)
from django import forms
from django.db import transaction
from django.utils.translation import gettext as _

from apps.study.models import ExerciseAvailability, ExerciseReward
from apps.users.models import Mentorship

from ..models import AssignedCalculationCondition, CalculationCondition

# -----------------------------------------------
# Form field configuration
# -----------------------------------------------


class MentorshipChoiceField(forms.ModelChoiceField):  # type: ignore
    """Field for student name display of mentorship instance."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the field."""
        kwargs.setdefault('label', _('Student'))
        kwargs.setdefault('required', True)
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]

    def label_from_instance(self, obj: Mentorship) -> str:
        """Display student name for mentorship relationship."""
        return str(obj.student)


# -----------------------------------------------
# Related models forms
# -----------------------------------------------


class ExerciseAvailabilityForm(forms.ModelForm):  # type: ignore
    """Exercise availability form."""

    class Meta:
        """Form configuration."""

        model = ExerciseAvailability
        fields = ['count', 'period']


class ExerciseRewardForm(forms.ModelForm):  # type: ignore
    """Exercise reward form."""

    class Meta:
        """Form configuration."""

        model = ExerciseReward
        fields = ['amount']


# -----------------------------------------------
# Calculation assignation main form
# -----------------------------------------------


# TODO: Add filling of related models on update
class AssignCalculationForm(forms.ModelForm):  # type: ignore
    """Assign calculation exercise form."""

    class Meta:
        """Form configuration."""

        model = AssignedCalculationCondition
        fields = ['calculation_condition', 'mentorship']

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        self.user = kwargs.pop('user')
        form_action = kwargs.pop('form_action')
        super().__init__(*args, **kwargs)  # type: ignore

        # - Exercise availability fields -
        self.availability_form = ExerciseAvailabilityForm()
        self.fields['count'] = self.availability_form.fields['count']
        self.fields['period'] = self.availability_form.fields['period']

        # - Exercise reward fields -
        self.reward_form = ExerciseRewardForm()
        self.fields['amount'] = self.reward_form.fields['amount']

        # - Exercise fields -
        exercises = CalculationCondition.objects.filter(user=self.user)  # type: ignore
        students = Mentorship.objects.filter(mentor=self.user)  # type: ignore
        self.fields['mentorship'] = MentorshipChoiceField(queryset=students)
        self.fields['calculation_condition'].queryset = exercises  # type: ignore
        self.fields['calculation_condition'].label = _('Exercise')

        # - Form helper -
        self.helper = FormHelper()
        self.helper.form_id = 'form'
        self.helper.form_action = form_action

        # - HTMX configuration -
        self.helper.attrs = {
            'hx-post': form_action,
            'hx-target': '#table-form-block',
            'hx-swap': 'innerHTML',
        }

        # - Form layout -
        self.helper.layout = Layout(
            Row(
                Column('mentorship'),
                Column('calculation_condition'),
            ),
            Row(
                Column('count'),
                Column('period'),
                Column('amount'),
            ),
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
                ),
                css_class='d-flex gap-2 justify-content-end',
            ),
        )

    def save(self, commit: bool = True) -> AssignedCalculationCondition:
        """Save calculation assignation."""
        try:
            with transaction.atomic():
                exercise = super().save(commit)

                if commit:
                    mentorship = self.cleaned_data['mentorship']

                    # Save exercise availability
                    availability = ExerciseAvailability()
                    availability.count = self.cleaned_data['count']
                    availability.period = self.cleaned_data['period']
                    availability.user = mentorship.student
                    availability.exercise = exercise
                    availability.save()

                    # Save exercise reward
                    reward = ExerciseReward()
                    reward.amount = self.cleaned_data['amount']
                    reward.mentorship = mentorship
                    reward.exercise = exercise
                    reward.save()

                return exercise  # type: ignore[no-any-return]

        except Exception as e:
            raise forms.ValidationError(
                f'Save exercise error: {str(e)}'
            ) from e
