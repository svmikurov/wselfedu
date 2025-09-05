"""Defines mathematical exercise conditions."""

from django.db import models


class ExerciseCondition(models.Model):
    """Mathematical exercise conditions."""

    name = models.CharField(
        'Наименование',
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

        verbose_name = 'Условие задания'
        verbose_name_plural = 'Условия заданий'
        db_table = 'math_exercise_condition'
        constraints = [
            models.CheckConstraint(
                name='max_gt_min',
                condition=models.Q(max_operand__gt=models.F('min_operand')),
            )
        ]

    def __str__(self) -> str:
        """Return string representation of model instance."""
        return str(self.name)
