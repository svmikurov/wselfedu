from django import forms

from english.models import CategoryModel, SourceModel


WORD_STUDY_STAGE_CHOICE = [
    ('AL', 'Все'),  # all
    ('WS', 'Изучение'),  # word study
    ('CK', 'Повторение'),  # consolidation of knowledge
    ('CH', 'Проверка'),  # check of knowledge
]
KNOWLEDGE_ASSESSMENT = (
    ('L', 'Изучаю'),        # learn
    ('R', 'Повторяю'),      # repeat
    ('C', 'Проверяю'),      # check
    ('K', 'Знаю'),          # know
)
WORD_COUNT = (
    ('OW', 'Слово'),
    ('CB', 'Словосочетание'),
    ('PS', 'Часть предложения'),
    ('ST', 'Предложение'),
)


PERIOD_START = (
    ('DT', 'Сегодня'), ('D3', 'Три дня назад'),
    ('W1', 'Неделя назад'), ('W4', 'Четыре недели назад'),
)
PERIOD_END = (
    ('DT', 'Сегодня'), ('D3', 'Три дня назад'),
    ('W1', 'Неделя назад'), ('W4', 'Четыре недели назад'),
    ('NC', 'Не выбран')
)

ATTR_CHECKBOX = {'class': 'form-check form-check-inline'}
"""Атрибут tag html, стиль для формы чекбокс.
"""


class WordLookupParamsForm(forms.Form):
    """Форма получения параметров выборки слов для упражнения изучения слов."""

    favorite_word = forms.BooleanField(
        required=False,
        help_text='Только избранные слова',
        widget=forms.CheckboxInput()
    )
    word_category = forms.ModelChoiceField(
        queryset=CategoryModel.objects.all(),
        empty_label='Категория',
        required=False,
        label='',
    )
    word_source = forms.ModelChoiceField(
        queryset=SourceModel.objects.all(),
        empty_label='Источник',
        required=False,
        label='',
    )
    period_start_date = forms.ChoiceField(
        choices=PERIOD_START,
        initial='W1',
        label='Период добавления (обновления) слова',
    )
    period_end_date = forms.ChoiceField(
        choices=PERIOD_END,
        initial='DT',
        label='',
    )
    word_count = forms.MultipleChoiceField(
        choices=WORD_COUNT,
        widget=forms.CheckboxSelectMultiple(),
        initial=('OW', 'CB'),
    )
    knowledge_assessment = forms.MultipleChoiceField(
        choices=KNOWLEDGE_ASSESSMENT,
        widget=forms.CheckboxSelectMultiple(),
        initial='L'
    )