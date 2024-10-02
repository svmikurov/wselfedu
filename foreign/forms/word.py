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
    CATEGORY,
    COL_6,
    FOREIGN_WORD,
    RUSSIAN_WORD,
    SOURCE,
    WORD_COUNT,
)
from foreign.models import Word


class WordForm(ModelForm):
    """Form for adding and updating a word."""

    class Meta:
        """Word model fields."""

        model = Word
        fields = (
            FOREIGN_WORD,
            RUSSIAN_WORD,
            CATEGORY,
            SOURCE,
            WORD_COUNT,
        )

    @staticmethod
    def apply_crispy_helper(form: Type[Form]) -> FormHelper:
        """Apply crispy form helper for specified WordModel form."""
        form.helper = FormHelper()
        form.helper.layout = Layout(
            Field(FOREIGN_WORD, autofocus=True),
            Field(RUSSIAN_WORD),
            Row(
                Column(CATEGORY, css_class=COL_6),
                Column(SOURCE, css_class=COL_6),
            ),
            Field(WORD_COUNT),
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
