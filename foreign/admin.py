"""Representation of models in the admin interface."""

from django.contrib import admin

from foreign.models import (
    TranslateParams,
    Word,
    WordAnalytics,
    WordCategory,
    WordProgress,
    WordSource,
)


@admin.register(WordAnalytics)
class WordAnalyticsAdmin(admin.ModelAdmin):
    """Representation of WordAnalytics in the admin interface."""

    list_display = ['word', 'display_count']
    """Fields to display.
    """
    ordering = ['-display_count']
    """Ordering.
    """


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    """Representation of WordModel in admin interface."""

    list_display = [
        'id',
        'foreign_word',
        'native_word',
        'created_at',
        'category',
        'user',
    ]
    """Fields to display (`list[str]`).
    """
    ordering = [
        'user',
        'id',
    ]
    """Ordering by fields (`list[str]`).
    """
    date_hierarchy = 'created_at'
    """Date hierarchy (`str`).
    """


@admin.register(WordCategory)
class WordCategoryAdmin(admin.ModelAdmin):
    """Representation of WordCategory in admin interface."""

    list_display = [
        'id',
        'name',
        'user',
    ]
    """Fields to display (`list[str]`).
    """
    ordering = [
        'user',
        'id',
    ]
    """Ordering by fields (`list[str]`).
    """


@admin.register(WordSource)
class WordSourceAdmin(admin.ModelAdmin):
    """Representation of WordSource in admin interface."""

    list_display = [
        'id',
        'name',
        'user',
    ]
    """Fields to display (`list[str]`).
    """
    ordering = [
        'user',
        'id',
    ]
    """Ordering by fields (`list[str]`).
    """


@admin.register(WordProgress)
class WordProgressAdmin(admin.ModelAdmin):
    """Representation of WordProgress in admin interface."""

    list_display = [
        'id',
        'word',
        'user',
        'progress',
    ]
    """Fields to display (`list[str]`).
    """
    ordering = [
        'user',
        'word',
    ]
    """Ordering by fields (`list[str]`).
    """


@admin.register(TranslateParams)
class WordParamsAdmin(admin.ModelAdmin):
    """Representation of WordParams in the admin interface."""

    list_display = [
        'user',
        'language_order',
        'timeout',
        'favorites',
        'category',
        'source',
        'progress',
        'word_count',
        'period_start_date',
        'period_end_date',
    ]
    """Fields to display.
    """
