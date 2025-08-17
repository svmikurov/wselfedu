"""Defines math app model administration."""

from django.contrib import admin

from .models import ExerciseCondition, MathExercise


@admin.register(MathExercise)
class MathExerciseAdmin(admin.ModelAdmin):  # type: ignore
    """Math app exercise model administration."""

    list_display = ['name']
    ordering = ['id']


@admin.register(ExerciseCondition)
class ExerciseConditionAdmin(admin.ModelAdmin):  # type: ignore
    """Math app exercise conditions model administration."""

    list_display = [
        'name',
        'conditions',
        'min_operand',
        'max_operand',
        'updated_at',
    ]
