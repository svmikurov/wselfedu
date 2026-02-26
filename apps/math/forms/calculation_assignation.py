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
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.utils.translation import gettext as _

from apps.study.models import ExerciseAvailability, ExerciseReward
from apps.users.models import Mentorship

from ..models import CalculationCondition, StudentCalculationCondition

type _RelatedModel = ExerciseAvailability | ExerciseReward

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
        fields = ['required_count', 'period_type']


class ExerciseRewardForm(forms.ModelForm):  # type: ignore
    """Exercise reward form."""

    class Meta:
        """Form configuration."""

        model = ExerciseReward
        fields = ['amount', 'reward_type']


# -----------------------------------------------
# Calculation assignation main form
# -----------------------------------------------


class AssignCalculationForm(forms.ModelForm):  # type: ignore
    """Assign calculation exercise form."""

    class Meta:
        """Form configuration."""

        model = StudentCalculationCondition
        fields = ['calculation_condition', 'mentorship']

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        self.user = kwargs.pop('user')
        self.form_action = kwargs.pop('form_action')
        super().__init__(*args, **kwargs)  # type: ignore

        self._add_related_form_fields()
        self._setup_fields()
        self._layout_form()

    def save(self, commit: bool = True) -> StudentCalculationCondition:
        """Save calculation assignation."""
        try:
            with transaction.atomic():
                exercise = super().save(commit)

                if commit:
                    mentorship = self.cleaned_data['mentorship']
                    content_type = ContentType.objects.get_for_model(exercise)

                    # Save exercise availability
                    self.availability_form.instance.user = mentorship.student
                    self.availability_form.instance.exercise_content_type = (
                        content_type
                    )
                    self.availability_form.instance.exercise_object_id = (
                        exercise.pk
                    )
                    self.availability_form.save()

                    # Save exercise reward
                    self.reward_form.instance.mentorship = mentorship
                    self.reward_form.instance.exercise_content_type = (
                        content_type
                    )
                    self.reward_form.instance.exercise_object_id = exercise.pk
                    self.reward_form.save()

                return exercise  # type: ignore[no-any-return]

        except Exception as e:
            raise forms.ValidationError(
                f'Save exercise error: {str(e)}'
            ) from e

    def _setup_fields(self) -> None:
        # - Exercise fields -
        exercises = CalculationCondition.objects.filter(user=self.user)  # type: ignore
        students = Mentorship.objects.filter(mentor=self.user)  # type: ignore
        self.fields['mentorship'] = MentorshipChoiceField(queryset=students)
        self.fields['calculation_condition'].queryset = exercises  # type: ignore
        self.fields['calculation_condition'].label = _('Exercise')

    def _layout_form(self) -> None:
        # - Form helper -
        self.helper = FormHelper()
        self.helper.form_id = 'form'
        self.helper.form_action = self.form_action

        # - HTMX configuration -
        self.helper.attrs = {
            'hx-post': self.form_action,
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
                Column('required_count'),
                Column('period_type'),
                css_class='align-items-end',
            ),
            Row(
                Column('reward_type'),
                Column('amount'),
                css_class='align-items-end',
            ),
            Div(
                Button(
                    'cancel',
                    _('button.cancel'),
                    css_class='wse-btn',
                    onclick=f"""
                    document.getElementById({self.helper.form_id!r}).remove()
                    """,
                ),
                Submit(
                    'submit',
                    _('button.submit'),
                    css_class='wse-btn',
                ),
                css_class='d-flex gap-2 justify-content-end',
            ),
        )

    def _add_related_form_fields(self) -> None:
        # - Get related instances for update event -
        if self.instance.pk:
            exercise_content_type = ContentType.objects.get_for_model(
                self.instance
            )
            try:
                availability_instance = ExerciseAvailability.objects.get(
                    exercise_content_type=exercise_content_type,
                    exercise_object_id=self.instance.pk,
                )
            except ExerciseAvailability.DoesNotExist:
                pass

            try:
                reward_instance = ExerciseReward.objects.get(
                    exercise_content_type=exercise_content_type,
                    exercise_object_id=self.instance.pk,
                )
            except ExerciseReward.DoesNotExist:
                pass
        else:
            availability_instance = None
            reward_instance = None

        # - Get related form -
        self.availability_form = ExerciseAvailabilityForm(
            instance=availability_instance,
            data=self.data if self.is_bound else None,
        )
        self.reward_form = ExerciseRewardForm(
            instance=reward_instance,
            data=self.data if self.is_bound else None,
        )

        # - Add related form fields to current form -
        self.fields.update(self.availability_form.fields)
        self.fields.update(self.reward_form.fields)

        # - Copy initial values from related forms -
        self.initial.update(self.availability_form.initial)
        self.initial.update(self.reward_form.initial)
