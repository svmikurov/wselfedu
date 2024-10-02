"""Representation of models in the admin interface."""

from django.contrib import admin

from config.constants import (
    CATEGORY,
    CREATED_AT,
    DISPLAY_COUNT,
    FOREIGN_WORD,
    RUSSIAN_WORD,
    SOURCE,
    USER,
    WORD,
)
from foreign.models import Word, WordAnalytics, WordParams


@admin.register(WordAnalytics)
class WordAnalyticsAdmin(admin.ModelAdmin):
    """Representation of WordAnalytics in the admin interface."""

    list_display = [WORD, DISPLAY_COUNT]
    """Fields to display.
    """
    ordering = ['-display_count']
    """Ordering.
    """


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    """Representation of WordModel in admin interface."""

    exclude = [USER]
    list_display = [
        FOREIGN_WORD,
        RUSSIAN_WORD,
        CREATED_AT,
        SOURCE,
        CATEGORY,
    ]
    """Fields to display.
    """


@admin.register(WordParams)
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
        'date_start',
        'date_end',
    ]
    """Fields to display.
    """
