"""Translation form."""

from crispy_forms.helper import FormHelper  # type: ignore
from crispy_forms.layout import Field, Layout, Submit  # type: ignore
from django import forms

from .. import models


class EnglishTranslationCreateForm(forms.Form):
    """Form to create translation of English word."""

    native = forms.CharField(
        max_length=models.EnglishWord.WORD_LENGTH,
    )
    english = forms.CharField(
        max_length=models.NativeWord.WORD_LENGTH,
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


class EnglishTranslationUpdateForm(forms.ModelForm):  # type: ignore[type-arg]
    """Form to update translation of English word."""

    native = forms.CharField(
        max_length=models.EnglishWord.WORD_LENGTH,
    )
    english = forms.CharField(
        max_length=models.NativeWord.WORD_LENGTH,
    )

    class Meta:
        """Form configuration."""

        model = models.EnglishTranslation
        fields: list[str] = []

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]

        if self.instance and self.instance.pk:
            self.fields['native'].initial = str(self.instance.native)
            self.fields['english'].initial = str(self.instance.english)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('native'),
            Field('english'),
            Submit('submit', 'Изменить'),
        )
