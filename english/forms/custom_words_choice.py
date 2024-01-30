from django import forms

# Поля, которые обрабатывают отношения - то, что надо
# https://docs.djangoproject.com/en/4.2/ref/forms/fields/#fields-which-handle-relationships


class WordsChooseForm(forms.Form):
    """Форма критериев выбора слов для изучения."""

    # Выбери, если только избранные слова.
    is_favorite = forms.BooleanField(
        label='Только избранные слова',
    )

    # Выбери из списка.
    category = forms.ChoiceField(
        label='',
        help_text='Выбери категорию',
    )
    source = forms.ChoiceField(
        label='',
        help_text='Выбери источник',
    )

    # Выбери период добавление слова.
    start_date = forms.DateField(
        label='Слово добавлено после даты',
    )
    final_date = forms.DateField(
        label='Слово добавлено до даты',
    )

    # Выбери количество слов.
    is_word = forms.BooleanField(
        label='Слово',
        initial=True,
    )
    is_phrase = forms.BooleanField(
        label='Словосочетание',
    )
    is_part_sentence = forms.BooleanField(
        label='Часть предложения',
    )
    is_sentence = forms.BooleanField(
        label='Предложение',
    )

    # Выбери уровень знания слов.
    is_studying = forms.BooleanField(
        label='Слово',
    )
    is_repetition = forms.BooleanField(
        label='Словосочетание',
    )
    is_examination = forms.BooleanField(
        label='Часть предложения',
    )
    is_learned = forms.BooleanField(
        label='Предложение',
    )
