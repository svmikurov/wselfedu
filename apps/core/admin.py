"""Defines Core app model administration."""

from django.apps import apps
from django.contrib import admin

from .models import Discipline, Exercise, TaskIO
from .models.base import BaseExercise


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Discipline model administration."""

    list_display = [
        'name',
        'slug',
        'id',
    ]
    ordering = [
        'name',
    ]


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Exercise model administration."""

    list_display = [
        'name',
        'discipline',
        'slug',
        'task_io',
        'content_object_display',
        'content_type_display',
        # Exercise id in exercise model of specific app (type content)
        'object_id',
        'id',
    ]

    def content_type_display(self, obj: Exercise) -> str:
        """Get discipline name."""
        content_type = obj.content_type
        if content_type:
            app_config = apps.get_app_config(obj.content_type.app_label)
            return str(app_config.verbose_name)
        return '-'

    def content_object_display(self, obj: Exercise) -> str:
        """Get exercise name."""
        exercise: BaseExercise = obj.content_object  # type: ignore[assignment]
        if exercise:
            return str(exercise.name)
        return '-'

    content_object_display.short_description = 'Вид упражнения'  # type: ignore[attr-defined]
    content_type_display.short_description = 'Приложение'  # type: ignore[attr-defined]


@admin.register(TaskIO)
class TaskIOAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Task I/O administration."""

    list_display = [
        'name',
        'alias',
        'id',
    ]
    ordering = [
        'name',
    ]
