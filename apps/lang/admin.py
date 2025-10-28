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

    list_display = ['user', 'english', 'native', 'created_at']


@admin.register(models.LangLabel)
class LangLabelAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Lang app label model administration."""

    list_display = ['name']


@admin.register(models.LangCategory)
class LangCategoryAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Lang app category model administration."""

    list_display = ['name']
