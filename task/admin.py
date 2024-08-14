"""Task app models admin interface representation module."""

from django.contrib import admin

from task.models import EnglishTaskSettings


@admin.register(EnglishTaskSettings)
class EnglishTaskSettingsAdmin(admin.ModelAdmin):
    """Representation of model in the admin interface."""

    list_display = [
        'user',
        'language_order',
        'timeout',
        'favorites',
        'category',
        'source',
        'knowledge',
        'word_count',
        'date_start',
        'date_end',
    ]
