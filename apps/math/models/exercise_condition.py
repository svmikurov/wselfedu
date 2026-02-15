"""Defines mathematical exercise conditions."""

from django.db import models
from django.utils.translation import gettext as _


class CalculationCondition(models.Model):
    """Calculation exercise conditions."""

    MAX_NAME_LENGTH = 100

    name = models.CharField(
        _('Exercise name'),
        max_length=MAX_NAME_LENGTH,
    )
    min_operand = models.SmallIntegerField(
        _('Min operand value'),
    )
    max_operand = models.SmallIntegerField(
        _('Max operand value'),
    )

    user = models.ForeignKey(
        'users.Person',
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _('Updated_at'),
        auto_now=True,
    )

    class Meta:
        """Model configurations."""

        verbose_name = _('Calculation exercise condition')
        verbose_name_plural = _('Calculation exercise conditions')
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
