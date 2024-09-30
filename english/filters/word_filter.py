"""Word filter module."""

import django_filters
from django import forms
from django.db.models import F, Q
from django.db.models.query import QuerySet
from django.forms import TextInput
from django.http import HttpRequest

from english.models import (
    CategoryModel,
    SourceModel,
)
from english.orm_queries.word_knowledge_assessment import (
    PROGRESS_STAGE_EDGES,
)


def category_by_current_user(request: HttpRequest) -> QuerySet:
    """Return only user categories."""
    if request is None:
        return CategoryModel.objects.none()
    return CategoryModel.objects.filter(user=request.user)


def source_by_current_user(request: HttpRequest) -> QuerySet:
    """Return only users sources."""
    if request is None:
        return SourceModel.objects.none()
    return SourceModel.objects.filter(user=request.user)


class WordsFilter(django_filters.FilterSet):
    """Word filter."""

    WORD_COUNT = (
        ('OW', 'Слово'),
        ('CB', 'Словосочетание'),
        ('PS', 'Часть предложения'),
        ('ST', 'Предложение'),
        ('NC', 'Не указано'),
    )
    WORD_STUDY_STAGE = (
        ('S', 'Изучаю'),  # study
        ('R', 'Повторяю'),  # repeat
        ('E', 'Проверяю'),  # examination
        ('K', 'Знаю'),  # know
    )

    search_word = django_filters.CharFilter(
        method='filter_word_by_any_translation',
        field_name='word_eng',
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
    filtered_study_stage = django_filters.ChoiceFilter(
        choices=WORD_STUDY_STAGE,
        method='get_filtered_study_stage',
        label='',
        empty_label='Стадия изучения слова',
    )

    only_favorite_words = django_filters.BooleanFilter(
        field_name='Только избранные слова',
        method='get_user_favorite_words',
        widget=forms.CheckboxInput,
        label='Только избранные слова',
    )

    @staticmethod
    def filter_word_by_any_translation(
        queryset: QuerySet,
        name: object,
        value: object,
    ) -> QuerySet:
        """Find a word in English or Russian."""
        return queryset.filter(
            Q(word_eng__icontains=value) | Q(word_rus__icontains=value)
        )

    @staticmethod
    def get_user_favorite_words(
        queryset: QuerySet,
        name: object,
        value: object,
    ) -> QuerySet:
        """Filter words by 'favorites' field."""
        if value:
            queryset = queryset.filter(
                wordsfavoritesmodel__word=F('pk'),
                wordsfavoritesmodel__user=F('user'),
            )
        return queryset

    @staticmethod
    def get_filtered_study_stage(
        queryset: QuerySet,
        name: object,
        value: object,
    ) -> QuerySet:
        """Filter words by study stage (knowledge_assessment)."""
        study = PROGRESS_STAGE_EDGES.get(value)
        qs = queryset.filter(
            worduserknowledgerelation__user_id=F('user'),
            worduserknowledgerelation__word_id=F('pk'),
            worduserknowledgerelation__knowledge_assessment__in=study,
        )
        return qs

    @staticmethod
    def get_filter_fields() -> tuple[str, ...]:
        """Get filter fields."""
        return (
            'search_word',
            'filtered_category',
            'filtered_source',
            'filtered_word_count',
            'filtered_study_stage',
            'only_favorite_words',
        )
