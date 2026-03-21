"""Assigned exercise model activation."""

from django.db import models

from apps.core.models.abstract import AbstractBaseModel


class ExerciseActive(AbstractBaseModel):
    """Active exercise status."""

    class IsActive(models.IntegerChoices):
        """Activation action choice."""

        ACTIVATED = (1, 'Activated')
        DEACTIVATED = (0, 'Deactivated')

    exercise = models.ForeignKey(
        'ExerciseAssigned',
        on_delete=models.CASCADE,
        verbose_name='Assigned exercise',
        related_name='activation_status',
    )
    is_active = models.BooleanField(
        choices=IsActive.choices,
        default=IsActive.DEACTIVATED,
        verbose_name='Activate status',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Active exercise status'
        verbose_name_plural = 'Active exercise statuses'
        db_table = 'study_assigned_active'
