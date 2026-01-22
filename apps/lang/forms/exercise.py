"""Language exercise forms."""

from crispy_forms.helper import FormHelper  # type: ignore[import-untyped]
from crispy_forms.layout import Layout  # type: ignore[import-untyped]
from django import forms
from django.utils.translation import gettext as _

from apps.core.forms import layouts
from apps.users import models as user_models
from apps.users.models import Person

from .. import models

# HACK: Add centralized management of discipline IDs
LANGUAGE_DISCIPLINE_ID = 2


class LangExerciseForm(forms.ModelForm):  # type: ignore
    """Language exercise from."""

    class Meta:
        """Form configuration."""

        model = models.LangExercise
        fields = ['name']

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        user = kwargs.pop('user', None)
        if not isinstance(user, Person):
            raise TypeError('Expected `Person` type')
        self.user = user

        form_action = kwargs.pop('form_action', None)
        if form_action is None:
            raise AttributeError('Expected form action')

        super().__init__(*args, **kwargs)  # type: ignore

        self.helper = FormHelper()
        self.helper.form_id = 'exercise-form'
        self.helper.form_action = form_action
        self.helper.layout = Layout(
            'name',
            layouts.create_button_row(self.helper.form_id),
        )

    def save(self, commit: bool = True) -> models.LangExercise:
        """Add user to model."""
        instance = super().save(commit=False)
        instance.discipline_id = LANGUAGE_DISCIPLINE_ID

        if self.user:
            instance.user = self.user

        if commit:
            instance.save()
        return instance  # type: ignore[no-any-return]


class ExerciseAssignationForm(forms.ModelForm):  # type: ignore[type-arg]
    """Exercise assignation form."""

    class Meta:
        """Form configuration."""

        model = models.EnglishAssignedExercise
        fields = ['mentorship', 'exercise']

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        user = kwargs.pop('user', None)
        if not isinstance(user, Person):
            raise TypeError('Expected `Person` type')
        self.user = user

        form_action = kwargs.pop('form_action', None)
        if form_action is None:
            raise AttributeError('Expected form action')

        super().__init__(*args, **kwargs)  # type: ignore

        self.fields['exercise'].empty_label = _('Select the exercise')  # type: ignore[attr-defined]

        self.fields['mentorship'] = forms.ModelChoiceField(
            queryset=user_models.Mentorship.objects.filter(
                mentor=self.user,
            ),
            label=_('Student'),
            empty_label=_('Select the student'),
        )
        self.fields['mentorship'].label_from_instance = lambda obj: str(  # type: ignore[attr-defined]
            obj.student
        )

        self.helper = FormHelper()
        self.helper.form_id = 'exercise-form'
        self.helper.form_action = form_action
        self.helper.layout = Layout(
            'exercise',
            'mentorship',
            layouts.create_button_row(self.helper.form_id),
        )
