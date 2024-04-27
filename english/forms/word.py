from django.forms import ModelForm, TextInput

from english.models import WordModel


class WordForm(ModelForm):
    """Форма добавления и изменения слова."""

    class Meta:
        model = WordModel
        fields = (
            'words_eng',
            'words_rus',
            'category',
            'source',
            'word_count',
        )
        # https://docs.djangoproject.com/en/5.0/topics/forms/modelforms/#overriding-the-default-fields
        widgets = {
            'words_eng': TextInput(attrs={'autofocus': True})
        }
