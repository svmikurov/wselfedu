"""Defines math app model administration."""

from django.contrib import admin

from apps.math.models import MathExercise


@admin.register(MathExercise)
class MathExerciseAdmin(admin.ModelAdmin):  # type: ignore
    """Math app exercise model administration."""

    list_display = ['name']
    ordering = ['name']
