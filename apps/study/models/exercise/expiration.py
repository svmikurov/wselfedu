"""Exercise expiration."""

from django.db import models

from apps.core.models.abstract import AbstractBaseModel


class ExerciseExpiration(AbstractBaseModel):
    """Expiry date of the exercise execution."""

    exercise = models.ForeignKey(
        'ExerciseAssigned',
        on_delete=models.CASCADE,
        verbose_name='Assigned exercise',
        related_name='exercise_expiration',
    )
    is_daily = models.BooleanField(
        default=False,
        verbose_name='Is daily exercise',
    )
    expiration = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Expiration date',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Exercise completion expiration'
        verbose_name_plural = 'Exercise completion expirations'
        db_table = 'study_assigned_expiration'
