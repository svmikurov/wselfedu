"""Language discipline models administration."""

from django.contrib import admin

from apps.lang import models


@admin.register(models.LangExercise)
class LangExerciseAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Lang app exercise model administration."""

    list_display = ['name']


@admin.register(models.NativeWord)
class NativeWordAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Native word model administration."""

    list_display = ['user', 'word', 'created_at']


@admin.register(models.EnglishWord)
class EnglishWordAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """English word model administration."""

    list_display = ['user', 'word', 'created_at']


@admin.register(models.EnglishTranslation)
class EnglishTranslationAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """English translation model administration."""

    list_display = [
        'user',
        'english',
        'native',
        'progress',
        'created_at',
        'category',
        'source',
    ]


@admin.register(models.LangMark)
class LangMarkAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Lang app mark model administration."""

    list_display = ['name']


@admin.register(models.LangCategory)
class LangCategoryAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Lang app category model administration."""

    list_display = ['name']


@admin.register(models.Parameters)
class ParametersAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Word study parameters model administration."""

    list_display = [
        'user',
        'category',
        'mark',
        'start_period',
        'end_period',
    ]


@admin.register(models.TranslationSetting)
class TranslationSettingAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Translation study settings model administration."""

    list_display = [
        'user',
        'translation_order',
        'word_count',
    ]


@admin.register(models.PresentationSettings)
class PresentationSettingsAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Presentation settings model administration."""

    list_display = [
        'user',
        'question_timeout',
        'answer_timeout',
    ]
