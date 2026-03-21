"""Assigned exercise."""

from django.db import models

from apps.core.models.abstract import AbstractBaseModel
from apps.core.models.exercise import Exercise
from apps.users.models import Mentorship


class ExerciseAssigned(AbstractBaseModel):
    """Assigned exercise to student by mentor the model."""

    mentorship = models.ForeignKey(
        Mentorship,
        on_delete=models.CASCADE,
        related_name='exercises',
        verbose_name='Mentorship',
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name='assigned_exercise',
        verbose_name='Assigned exercise',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Assigned exercise'
        verbose_name_plural = 'Assigned exercises'
        db_table = 'study_assigned'
        indexes = [models.Index(fields=['mentorship', 'exercise'])]

    def __str__(self) -> str:
        """Get the string representation of model instance."""
        return str(self.exercise)
