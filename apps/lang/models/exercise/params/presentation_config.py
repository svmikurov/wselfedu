"""Presentation configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final, Self

from django.core import validators
from django.db import models

from apps.core.models import AbstractBaseModel

if TYPE_CHECKING:
    from apps.users.models import Person

__all__ = ('PresentationConfig',)


class PresentationConfig(AbstractBaseModel):
    """Presentation configuration model."""

    MIN_TIMEOUT: Final[int] = 1
    DEFAULT_TIMEOUT: Final[int] = 3
    MAX_TIMEOUT: Final[int] = 300

    user = models.ForeignKey(
        'users.Person',
        on_delete=models.CASCADE,
        verbose_name='User',
        related_name='user_presentation_configuration',
    )

    question_timeout = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        default=DEFAULT_TIMEOUT,
        validators=[
            validators.MinValueValidator(MIN_TIMEOUT),
            validators.MaxValueValidator(MAX_TIMEOUT),
        ],
        verbose_name='Task read time (sec)',
        help_text=f'From {MIN_TIMEOUT} to {MAX_TIMEOUT} seconds',
    )
    answer_timeout = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        default=DEFAULT_TIMEOUT,
        validators=[
            validators.MinValueValidator(MIN_TIMEOUT),
            validators.MaxValueValidator(MAX_TIMEOUT),
        ],
        verbose_name='Task completion time (sec)',
        help_text=f'From {MIN_TIMEOUT} to {MAX_TIMEOUT} seconds',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Presentation configuration'
        verbose_name_plural = 'Presentation configuration'

        # TODO: Add constrains after Period model improve
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                name='lang_presentation_config_unique_user_name',
            ),
        ]

        db_table = 'lang_presentation_config'

    @classmethod
    def get_instants(cls, user: Person) -> Self:
        """Get user presentation configurations or return defaults."""
        try:
            return cls.objects.get(user=user)
        except cls.DoesNotExist:
            return cls()
