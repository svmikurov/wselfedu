"""Mark form."""

from typing import Generic, TypeVar

from crispy_forms.helper import FormHelper  # type: ignore[import-untyped]
from crispy_forms.layout import Layout  # type: ignore[import-untyped]
from django import forms
from django.db.models import Model

from apps.users.models import Person

from .layouts import create_button_row

M = TypeVar('M', bound=Model)


class UserRelationForm(forms.ModelForm, Generic[M]):  # type: ignore
    """Base form with user relationship.

    Example:
    -------
        class SourceForm(BaseNameForm[Source]):

            class Meta:

                model = Source
                fields = [...]

        class SourceCreateView(BaseCreateView):

            template_name = 'components/crispy_form.html'
            form_class = SourceForm
            success_url = ...

    """

    FORM_ID = 'form'

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
        self.helper.form_id = self.FORM_ID

    def save(self, commit: bool = True) -> M:
        """Add user to model instance."""
        instance = super().save(commit=False)

        if self.user:
            instance.user = self.user

        if commit:
            instance.save()
        return instance  # type: ignore[no-any-return]


class BaseNameForm(UserRelationForm[M], Generic[M]):
    """Base user-name crispy form.

    Provides 'name' fields, adds user to model instants.

    Example:
    -------
        class SourceForm(BaseNameForm[Source]):

            class Meta:

                model = Source
                fields = ['name']

        class SourceCreateView(BaseCreateView):

            template_name = 'components/crispy_form.html'
            form_class = SourceForm
            success_url = ...

    """

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        super().__init__(*args, **kwargs)

        self.helper.layout = Layout(
            'name',
            create_button_row(self.helper.form_id),
        )
