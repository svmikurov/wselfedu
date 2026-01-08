"""Translation form."""

from crispy_forms.helper import FormHelper  # type: ignore
from crispy_forms.layout import (  # type: ignore
    HTML,
    Column,
    Layout,
    Row,
)
from django import forms
from django.db.models import QuerySet

from .. import models


class BaseEnglishForm(forms.ModelForm):  # type: ignore[type-arg]
    """Base foreign translation form."""

    native = forms.CharField(
        max_length=models.EnglishWord.WORD_LENGTH,
    )
    foreign = forms.CharField(
        max_length=models.NativeWord.WORD_LENGTH,
    )

    def clean_marks(self) -> list[models.LangMark] | None:
        """Convert QuerySet to list for cleaned_data."""
        marks = self.cleaned_data.get('marks')
        if not marks:
            return []
        if isinstance(marks, QuerySet):
            return list(marks)
        return marks  # type: ignore[no-any-return]

    class Meta:
        """Form configuration."""

        model = models.EnglishTranslation
        fields: list[str] = ['category', 'source', 'marks']


class EnglishCreateForm(BaseEnglishForm):
    """Form to create translation of English word."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]
        self.fields['native'].label = 'Слово на русском'
        self.fields['foreign'].label = 'Слово на английском'

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('native'),
                Column('foreign'),
            ),
            Row(
                Column('marks'),
                Column(
                    'category',
                    'source',
                    HTML("""
                        <div class="d-flex justify-content-end pt-2">
                            <button type="submit" name="submit"
                                    class="wse-btn">
                                Добавить
                            </button>
                        </div>
                    """),
                ),
            ),
        )


class EnglishUpdateForm(BaseEnglishForm):
    """Form to update translation of English word."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]
        self.fields['native'].label = 'Слово на русском'
        self.fields['foreign'].label = 'Слово на английском'

        if self.instance and self.instance.pk:
            self.fields['native'].initial = str(self.instance.native)
            self.fields['foreign'].initial = str(self.instance.foreign)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('native'),
                Column('foreign'),
            ),
            Row(
                Column('marks'),
                Column(
                    'category',
                    'source',
                    HTML("""
                        <div class="d-flex justify-content-end pt-2">
                            <button type="submit" name="submit"
                                    class="wse-btn">
                                Изменить
                            </button>
                        </div>
                    """),
                ),
            ),
        )
