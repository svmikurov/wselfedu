"""Mark form."""

from typing import Generic, TypeVar

from crispy_forms.helper import FormHelper  # type: ignore[import-untyped]
from crispy_forms.layout import Layout  # type: ignore[import-untyped]
from django import forms
from django.db.models import Model

from apps.users.models import Person

from .layouts import create_button_row

M = TypeVar('M', bound=Model)


class BaseNameForm(forms.ModelForm, Generic[M]):  # type: ignore
    """Base user-name crispy form.

    Provides 'name' fields, adds user to model instants.
    """

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
        self.helper.form_action = form_action
        self.helper.form_id = 'form'
        self.helper.layout = Layout(
            'name',
            create_button_row(self.helper.form_id),
        )

    def save(self, commit: bool = True) -> M:
        """Add user to model instance."""
        instance = super().save(commit=False)

        if self.user:
            instance.user = self.user

        if commit:
            instance.save()
        return instance  # type: ignore[no-any-return]
