"""Representation of models in the admin interface."""

from django.contrib import admin

from config.constants import (  # noqa: F401
    CATEGORY,
    CREATED_AT,
    DISPLAY_COUNT,
    FOREIGN_WORD,
    ID,
    MENTOR,
    NAME,
    NATIVE_WORD,
    PROGRESS,
    SOURCE,
    USER,
    WORD,
)
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

    list_display = [WORD, DISPLAY_COUNT]
    """Fields to display.
    """
    ordering = ['-display_count']
    """Ordering.
    """


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    """Representation of WordModel in admin interface."""

    exclude = [MENTOR]
    list_display = [
        ID,
        FOREIGN_WORD,
        NATIVE_WORD,
        CREATED_AT,
        CATEGORY,
        USER,
    ]  # fmt: skip
    """Fields to display.
    """
    ordering = [
        USER,
        ID,
    ]
    date_hierarchy = 'created_at'


@admin.register(WordCategory)
class WordCategoryAdmin(admin.ModelAdmin):
    """Representation of WordCategory in admin interface."""

    list_display = [
        ID,
        NAME,
        USER,
    ]
    ordering = [
        USER,
        ID,
    ]


@admin.register(WordSource)
class WordSourceAdmin(admin.ModelAdmin):
    """Representation of WordSource in admin interface."""

    list_display = [
        ID,
        NAME,
        USER,
    ]
    ordering = [
        USER,
        ID,
    ]


@admin.register(WordProgress)
class WordProgressAdmin(admin.ModelAdmin):
    """Representation of WordProgress in admin interface."""

    list_display = [
        ID,
        WORD,
        USER,
        PROGRESS,
    ]
    ordering = [
        USER,
        WORD,
    ]


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
