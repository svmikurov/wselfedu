"""Defines Lang app model administration."""

from django.contrib import admin

from apps.lang.models import LangExercise


@admin.register(LangExercise)
class LangExerciseAdmin(admin.ModelAdmin):
    """Lang app exercise model administration."""

    list_display = ['name']
