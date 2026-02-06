"""Abstract progress model."""

from django.db import models

__all__ = [
    'AbstractProgressModel',
]


class AbstractProgressModel(models.Model):
    """Abstract progress model."""

    DEFAULT_PROGRESS = 0

    progress = models.PositiveSmallIntegerField(
        default=DEFAULT_PROGRESS,
        verbose_name='Прогресс изучения',
    )

    class Meta:
        """Model configuration."""

        abstract = True
