"""Defines math app model administration."""

from django.contrib import admin

from .models import (
    ExerciseCondition,
    MathAssignedConditionRel,
    MathExercise,
)


@admin.register(MathExercise)
class MathExerciseAdmin(admin.ModelAdmin):  # type: ignore
    """Math exercise model administration."""

    list_display = [
        'name',
        'id',
    ]
    ordering = ['id']


@admin.register(ExerciseCondition)
class ExerciseConditionAdmin(admin.ModelAdmin):  # type: ignore
    """Math exercise condition model administration."""

    list_display = [
        'name',
        'min_operand',
        'max_operand',
        'updated_at',
    ]


@admin.register(MathAssignedConditionRel)
class ExerciseConditionRelAdmin(admin.ModelAdmin):  # type: ignore
    """Math exercise condition relationship model administration."""

    list_display = [
        'assignation__mentorship__mentor',
        'assignation__mentorship__student',
        'condition',
        'assignation__id',
        'assignation',
    ]
