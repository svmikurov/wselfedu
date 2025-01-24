"""Category form module."""

from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit
from django import forms

from foreign.models import WordCategory


class CategoryForm(forms.ModelForm):
    """Category list form."""

    is_active = forms.BooleanField(
        label='Активна',
        required=False,
    )
    name = forms.CharField(
        label='Наименование категории',
    )

    class Meta:
        """Add model with specific fields."""

        model = WordCategory
        fields = ('is_active', 'name')

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
            Submit('submit', 'Изменить', css_class='btn btn-success'),
            StrictButton(
                'Назад',
                css_class='btn btn-primary',
                onclick='history.back();',
            ),
        )
