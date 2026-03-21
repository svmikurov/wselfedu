"""Item study progress phase model."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q

if TYPE_CHECKING:
    type ProgressT = Literal['is_study', 'is_repeat', 'is_examine', 'is_know']


class ProgressBar(models.Model):
    """Progress bar version model."""

    # Max progress phase values for progress change scale
    STUDY_DEFAULT = 7
    REPEAT_DEFAULT = 10
    EXAMINE_DEFAULT = 16
    KNOW_DEFAULT = 17

    DEFAULT_PROGRESS_RANGES: dict[ProgressT, list[int]] = {
        'is_study': [*range(0, STUDY_DEFAULT + 1)],
        'is_repeat': [*range(STUDY_DEFAULT + 1, REPEAT_DEFAULT + 1)],
        'is_examine': [*range(REPEAT_DEFAULT + 1, EXAMINE_DEFAULT + 1)],
        'is_know': [KNOW_DEFAULT],
    }

    user = models.ForeignKey(
        'users.Person',
        on_delete=models.CASCADE,
        verbose_name='User',
        related_name='progresses',
    )
    name = models.CharField(
        max_length=30,
        help_text='Progress change scale name',
    )

    study = models.PositiveSmallIntegerField(
        default=STUDY_DEFAULT,
        verbose_name='Study',
        help_text="""
        Significance for the transition between the "Study-Repeat" stages
        """,
    )
    repeat = models.PositiveSmallIntegerField(
        default=REPEAT_DEFAULT,
        verbose_name='Repeat',
        help_text="""
        Significance for the transition between the "Repeat-Examine" stages
        """,
    )
    examine = models.PositiveSmallIntegerField(
        default=EXAMINE_DEFAULT,
        verbose_name='Examine',
        help_text="""
        Significance for the transition between the "Examine-Know" stages
        """,
    )
    know = models.PositiveSmallIntegerField(
        default=KNOW_DEFAULT,
        verbose_name='Know',
        help_text='Maximum progress value',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Progress of study'
        verbose_name_plural = 'Progress in learning'

        db_table = 'study_progress'

        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['user']),
        ]

        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(study__lt=F('repeat'))
                    & Q(repeat__lt=F('examine'))
                    & Q(examine__lt=F('know'))
                ),
                name='progress_study_lt_repeat_lt_examine_lt_know',
            ),
            models.UniqueConstraint(
                fields=['user', 'name'],
                name='unique_user_progress_name',
            ),
        ]

    def __str__(self) -> str:
        """Get string representation of progress instance."""
        return str(self.name)

    def clean(self) -> None:
        """Validate progress values on model level."""
        super().clean()

        if not (self.study < self.repeat < self.examine < self.know):
            raise ValidationError(
                {
                    'study': 'study < repeat',
                    'repeat': 'repeat < examine',
                    'examine': 'examine < know',
                    'know': 'Values ​​should increase from left to right',
                }
            )

        if (
            self.study < 0
            or self.repeat < 0
            or self.examine < 0
            or self.know < 0
        ):
            raise ValidationError('Progress values ​​cannot be negative')

    def save(self, *args: object, **kwargs: object) -> None:
        """Call clean() before saving."""
        self.full_clean()
        super().save(*args, **kwargs)  # type: ignore[arg-type]
