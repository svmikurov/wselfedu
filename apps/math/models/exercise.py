"""Defines math app exercise type model."""

from django.db import models

from apps.core.models.base import BaseExercise
from apps.users.models import ExerciseAssigned


class MathExercise(BaseExercise):
    """Math app exercise type model."""

    class Meta:
        """Model configuration."""

        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'

    def __str__(self) -> str:
        """Return string representation of model."""
        return str(self.name)


class ExerciseCondition(models.Model):
    """Mathematical exercise conditions."""

    conditions = models.ForeignKey(
        ExerciseAssigned,
        on_delete=models.CASCADE,
        verbose_name='Назначенное упражнение',
        related_name='math_condition',
    )
    name = models.CharField(
        'Наименование условия',
        max_length=100,
    )
    min_operand = models.SmallIntegerField(
        'Минимальное значение операнда',
    )
    max_operand = models.SmallIntegerField(
        'Максимальное значение операнда',
    )
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        'Изменено',
        auto_now=True,
    )

    class Meta:
        """Model configurations."""

        verbose_name = 'Условия вычисления'
        verbose_name_plural = 'Условия вычислений'
        db_table = 'math_exercise_condition'
        constraints = [
            models.CheckConstraint(
                name='max_gt_min',
                condition=models.Q(max_operand__gt=models.F('min_operand')),
            )
        ]
