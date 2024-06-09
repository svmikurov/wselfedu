from django.contrib import admin

from task.models import EnglishTaskSettings


@admin.register(EnglishTaskSettings)
class EnglishTaskSettingsAdmin(admin.ModelAdmin):
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
