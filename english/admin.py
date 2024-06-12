from django.contrib import admin

from english.models import WordLearningStories


class WordLearningStoriesAdmin(admin.ModelAdmin):
    """Representation of a ``WordLearningStoriesAdmin`` model in the
    admin interface.

    Attributes
    ----------
    list_display : `list[str]`
        List of model fields.
    ordering : `list[str]`
        Sorting by model field (descending ``list_display``, by
        default).
    """

    list_display = ['word', 'display_count']
    ordering = ['-display_count']


admin.site.register(WordLearningStories, WordLearningStoriesAdmin)
