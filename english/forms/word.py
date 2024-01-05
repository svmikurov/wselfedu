from django.forms import ModelForm

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
