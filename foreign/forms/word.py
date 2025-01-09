"""Word form module."""

from typing import Type

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Button,
    ButtonHolder,
    Column,
    Field,
    Layout,
    Reset,
    Row,
    Submit,
)
from django.forms import Form, ModelForm

from config.constants import (
    COL_6,
)
from foreign.models import Word


class WordForm(ModelForm):
    """Form for adding and updating a word."""

    class Meta:
        """Word model fields."""

        model = Word
        fields = (
            'foreign_word',
            'native_word',
            'category',
            'source',
        )

    @staticmethod
    def apply_crispy_helper(form: Type[Form]) -> FormHelper:
        """Apply crispy form helper for specified WordModel form."""
        form.helper = FormHelper()
        form.helper.layout = Layout(
            Field('foreign_word', autofocus=True),
            Field('native_word'),
            Row(
                Column('category', css_class=COL_6),
                Column('source', css_class=COL_6),
            ),
            ButtonHolder(
                Submit(
                    name='Save',
                    value='Сохранить',
                    css_class='btn-success btn-sm',
                    style='width:108px',
                ),
                Reset(
                    name='Reset This Form',
                    value='Сбросить',
                    css_class='btn-danger btn-sm',
                    style='width:108px',
                ),
                Button(
                    name='Back',
                    value='Назад',
                    css_class='btn-primary btn-sm',
                    style='width:108px',
                    onclick='history.back();',
                ),
            ),
        )
        return form
