"""Defines mathematical exercise conditions."""

from django.db import models
from django.utils.translation import gettext as _

from apps.core.models import AbstractBaseModel


class CalculationTypeChoices(models.TextChoices):
    """Calculation type choices."""

    ADD = 'add', _('Adding')
    SUB = 'sub', _('Submission')
    MUL = 'mul', _('Multiplication')
    DIV = 'div', _('Division')


class CalculationCondition(models.Model):
    """Calculation exercise conditions."""

    MAX_NAME_LENGTH = 100

    name = models.CharField(
        _('Exercise name'),
        max_length=MAX_NAME_LENGTH,
        unique=True,
    )
    min_operand = models.SmallIntegerField(
        _('Min operand value'),
    )
    max_operand = models.SmallIntegerField(
        _('Max operand value'),
    )
    operation_type = models.CharField(
        choices=CalculationTypeChoices,
        max_length=10,
        default=CalculationTypeChoices.ADD,
    )

    user = models.ForeignKey(
        'users.Person',
        on_delete=models.CASCADE,
        verbose_name=_('The user who created the exercise'),
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


class StudentCalculationCondition(AbstractBaseModel):
    """Assigned calculation conditions."""

    calculation_condition = models.ForeignKey(
        CalculationCondition,
        on_delete=models.CASCADE,
        verbose_name=_('Calculation condition'),
    )
    mentorship = models.ForeignKey(
        'users.Mentorship',
        on_delete=models.CASCADE,
        verbose_name=_('Mentorship'),
    )

    class Meta:
        """Model configurations."""

        verbose_name = _('Assigned calculation exercise condition')
        verbose_name_plural = _('Assigned calculation exercise conditions')

        db_table = 'math_exercise_condition_student'
