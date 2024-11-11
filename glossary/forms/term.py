"""Term term form."""

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
from django import forms

from config.constants import COL_6
from glossary.models import Term


class TermForm(forms.ModelForm):
    """Term term form."""

    class Meta:
        """Setup form."""

        model = Term
        fields = [
            'term',
            'translate',
            'definition',
            'interpretation',
            'category',
            'source',
        ]
        widgets = {
            'definition': forms.Textarea(attrs={'rows': 5}),
            'interpretation': forms.Textarea(attrs={'rows': 5}),
        }

    @staticmethod
    def apply_crispy_helper(form: Type[forms.Form]) -> FormHelper:
        """Apply crispy form helper for specified WordModel form."""
        form.helper = FormHelper()
        form.helper.layout = Layout(
            Field('term', autofocus=True),
            Field('translate'),
            Field('definition'),
            Field('interpretation'),
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
