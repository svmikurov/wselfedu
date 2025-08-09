"""Defines student study models."""

from typing import Any

from django.db import models

from apps.core.models.base import BaseExercise
from apps.core.models.exercise import Exercise
from apps.users.models import Mentorship

BASE_EXERCISE = BaseExercise


def get_subclasses_choices() -> dict[str, Any]:
    """Get exercise models for choice."""
    return {
        'model__in': [
            m._meta.model_name for m in BASE_EXERCISE.__subclasses__()
        ]
    }


class AssignedExercise(models.Model):
    """Assigned exercise to student by mentor the model."""

    mentorship = models.ForeignKey(
        Mentorship,
        on_delete=models.CASCADE,
        related_name='exercises',
        verbose_name='Наставничество',
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name='assigned_exercise',
        verbose_name='Назначенное упражнение',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата назначения',
    )

    class Meta:
        """Configure the model."""

        verbose_name = 'Назначенное упражнение'
        verbose_name_plural = 'Назначенные упражнения'

    def __str__(self) -> str:
        """Get the string representation of model instance."""
        return str(self.exercise)
