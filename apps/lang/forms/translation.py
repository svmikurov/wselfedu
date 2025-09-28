"""Translation form."""

from crispy_forms.helper import FormHelper  # type: ignore
from crispy_forms.layout import Field, Layout, Submit  # type: ignore
from django import forms

from ..models.word import WORD_LENGTH


class EnglishTranslationForm(forms.Form):
    """Form to create translation of English word."""

    native = forms.CharField(
        max_length=WORD_LENGTH,
    )
    english = forms.CharField(
        max_length=WORD_LENGTH,
    )

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('native'),
            Field('english'),
            Submit('submit', 'Добавить'),
        )
