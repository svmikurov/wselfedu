"""Word filter."""

import django_filters
from django import forms
from django.db.models import F, Q
from django.db.models.query import QuerySet
from django.forms import TextInput
from django.http import HttpRequest

from config.constants import (
    CATEGORY,
    EXACT,
    FOREIGN_WORD,
    ICONTAINS,
    PK,
    PROGRESS_CHOICES,
    SOURCE,
    USER,
    WORD_COUNT,
    WORD_COUNT_CHOICE,
)
from foreign.models import (
    WordCategory,
    WordSource,
)
from foreign.queries.progress import (
    PROGRESS_STAGE_EDGES,
)


def category_by_current_user(request: HttpRequest) -> QuerySet:
    """Return only user categories."""
    if request is None:
        return WordCategory.objects.none()
    return WordCategory.objects.filter(user=request.user)


def source_by_current_user(request: HttpRequest) -> QuerySet:
    """Return only users sources."""
    if request is None:
        return WordSource.objects.none()
    return WordSource.objects.filter(user=request.user)


class WordsFilter(django_filters.FilterSet):
    """Word filter."""

    search_word = django_filters.CharFilter(
        method='filter_word_by_any_translation',
        field_name=FOREIGN_WORD,
        lookup_expr='icontains',
        label='',
        widget=TextInput(attrs={'placeholder': 'Поиск по слову'}),
    )
    filtered_category = django_filters.ModelChoiceFilter(
        queryset=category_by_current_user,
        field_name=CATEGORY,
        lookup_expr=EXACT,
        label='',
        empty_label='Категория',
    )
    filtered_source = django_filters.ModelChoiceFilter(
        queryset=source_by_current_user,
        field_name=SOURCE,
        lookup_expr=EXACT,
        label='',
        empty_label='Источник',
    )
    filtered_word_count = django_filters.ChoiceFilter(
        choices=WORD_COUNT_CHOICE,
        field_name=WORD_COUNT,
        lookup_expr=ICONTAINS,
        label='',
        empty_label='Любое кол-во слов',
    )
    filtered_study_stage = django_filters.ChoiceFilter(
        choices=PROGRESS_CHOICES,
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
        """Find a word in foreign or native."""
        return queryset.filter(
            Q(foreign_word__icontains=value) | Q(native_word__icontains=value)
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
                wordfavorites__word=F(PK),
                wordfavorites__user=F(USER),
            )
        return queryset

    @staticmethod
    def get_filtered_study_stage(
        queryset: QuerySet,
        name: object,
        value: object,
    ) -> QuerySet:
        """Filter words by study stage (progress)."""
        study = PROGRESS_STAGE_EDGES.get(value)
        qs = queryset.filter(
            wordprogress__user_id=F(USER),
            wordprogress__word_id=F(PK),
            wordprogress__progress__in=study,
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