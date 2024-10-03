"""Representation of model in the admin interface."""

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
from english.models import WordLearningStories, WordModel


@admin.register(WordLearningStories)
class WordLearningStoriesAdmin(admin.ModelAdmin):
    """Representation of model in the admin interface.

    Attributes
    ----------
    list_display : `list[str]`
        List of model fields.
    ordering : `list[str]`
        Sorting by model field (descending ``list_display``, by
        default).

    """

    list_display = [WORD, DISPLAY_COUNT]
    ordering = ['-display_count']


@admin.register(WordModel)
class WordModelAdmin(admin.ModelAdmin):
    """Representation of WordModel in admin interface."""

    exclude = [USER]
    list_display = [
        FOREIGN_WORD,
        RUSSIAN_WORD,
        CREATED_AT,
        SOURCE,
        CATEGORY,
    ]
