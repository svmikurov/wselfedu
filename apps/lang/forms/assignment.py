"""Translation study assignment form."""

from django import forms

from apps.users.models import Person

from .. import models


class AssignTranslationForm(forms.Form):
    """Form to assign the translation to study."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        mentor = kwargs.pop('user', None)
        if not isinstance(mentor, Person):
            raise TypeError('Expected `Person` type')
        self.mentor = mentor
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]

        self.fields['exercise_id'] = forms.ModelChoiceField(
            queryset=models.LangExercise.objects.filter(
                user=self.mentor,
            ),
            label='Упражнение',
            widget=forms.Select(
                attrs={
                    'hx-get': '',
                    'hx-trigger': 'change',
                    'hx-target': '#translations-table',
                    'hx-swap': 'outerHTML',
                    'class': 'form-select',
                }
            ),
        )
