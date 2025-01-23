"""Category form module."""

from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Field, Layout, Submit
from django import forms
from django.forms import ModelForm

from foreign.models import WordCategory


class CategoryForm(ModelForm):
    """Category form class."""

    class Meta:
        """Add model with specific fields."""

        model = WordCategory
        fields = ('is_active', 'name')


class CategoryListForm(forms.Form):
    """Category list form."""

    is_active = forms.BooleanField(
        label='Активна',
        required=False,
    )
    name = forms.CharField(
        label='Имя категории',
    )

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form helper."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-categoryListForm'
        self.helper.form_class = 'blueForms'
        self.helper.method = 'post'
        self.helper.action = 'submit_survey'

        self.helper.layout = Layout(
            Field('is_active'),
            Field('name'),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white'),
            ),
        )
