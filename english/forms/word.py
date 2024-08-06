"""Word form module."""

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
from django.forms import ModelForm

from english.models import WordModel


class WordForm(ModelForm):
    """Form for adding and updating a word."""

    class Meta:
        """Word model fields."""

        model = WordModel
        fields = (
            'word_eng',
            'word_rus',
            'category',
            'source',
            'word_count',
        )

    @staticmethod
    def apply_crispy_helper(form):
        """Apply crispy form helper for specified WordModel form."""
        form.helper = FormHelper()
        form.helper.layout = Layout(
            Field('word_eng', autofocus=True),
            Field('word_rus'),
            Row(
                Column('category', css_class='col-6'),
                Column('source', css_class='col-6'),
            ),
            Field('word_count'),
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
