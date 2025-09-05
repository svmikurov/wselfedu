"""Defines Assigned math exercise condition relationship model."""

from django.db import models

from apps.math.models import ExerciseCondition
from apps.study.models import ExerciseAssigned


class MathAssignedConditionRel(models.Model):
    """Assigned math exercise condition relationship model."""

    assignation = models.OneToOneField(
        ExerciseAssigned,
        on_delete=models.CASCADE,
        related_name='math_condition_rel',
        verbose_name='Назначение',
    )
    condition = models.ForeignKey(
        ExerciseCondition,
        on_delete=models.CASCADE,
        related_name='math_assigned_conditions',
        verbose_name='Условие матем. задания',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Условие назначенного матем. задания'
        verbose_name_plural = 'Условия назначенного матем. задания'
        db_table = 'math_exercise_assigned_condition_rel'
