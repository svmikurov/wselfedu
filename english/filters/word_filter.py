import django_filters
from django.forms import TextInput

from english.models import (
    CategoryModel,
    SourceModel,
)


class WordsFilter(django_filters.FilterSet):
    """Words filter"""

    WORD_COUNT = (
        ('OW', 'Слово'),
        ('CB', 'Словосочетание'),
        ('PS', 'Часть предложения'),
        ('ST', 'Предложение'),
        ('NC', 'Не указано'),
    )

    search_word = django_filters.CharFilter(
        field_name='words_eng',
        lookup_expr='icontains',
        label='',
        widget=TextInput(attrs={'placeholder': 'Поиск по слову'}),
    )
    filtered_category = django_filters.ModelChoiceFilter(
        queryset=CategoryModel.objects.all(),
        field_name='category',
        lookup_expr='exact',
        label='',
        empty_label='Категория',
    )
    filtered_source = django_filters.ModelChoiceFilter(
        queryset=SourceModel.objects.all(),
        field_name='source',
        lookup_expr='exact',
        label='',
        empty_label='Источник',
    )
    filtered_word_count = django_filters.ChoiceFilter(
        choices=WORD_COUNT,
        field_name='word_count',
        lookup_expr='icontains',
        label='',
        empty_label='Любое кол-во слов',
    )
