import django_filters
from django import forms
from django.db.models import Q, F
from django.forms import TextInput

from english.models import (
    CategoryModel,
    SourceModel,
)


def category_by_current_user(request):
    if request is None:
        return CategoryModel.objects.none()
    return CategoryModel.objects.filter(user=request.user)


def source_by_current_user(request):
    if request is None:
        return SourceModel.objects.none()
    return SourceModel.objects.filter(user=request.user)


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
        method='filter_word_by_any_language',
        field_name='words_eng',
        lookup_expr='icontains',
        label='',
        widget=TextInput(attrs={'placeholder': 'Поиск по слову'}),
    )
    filtered_category = django_filters.ModelChoiceFilter(
        queryset=category_by_current_user,
        field_name='category',
        lookup_expr='exact',
        label='',
        empty_label='Категория',
    )
    filtered_source = django_filters.ModelChoiceFilter(
        queryset=source_by_current_user,
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

    only_favorite_words = django_filters.BooleanFilter(
        field_name='Только избранные слова',
        method='get_user_favorite_words',
        widget=forms.CheckboxInput,
        label='Только избранные слова',
    )

    def filter_word_by_any_language(self, queryset, name, value):
        return queryset.filter(
            Q(words_eng__icontains=value) | Q(words_rus__icontains=value)
        )

    def get_user_favorite_words(self, queryset, name, value):
        """Filter words by 'favorites' field."""
        if value:
            queryset = queryset.filter(
                wordsfavoritesmodel__word=F('pk'),
                wordsfavoritesmodel__user=F('user'),
            )
        return queryset
