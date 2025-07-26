"""Defines reward limits."""

from django.db import models


# TODO: Develop
class RewardLimit(models.Model):
    """Reward limits."""

    user = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
    )
    daily_limit = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )
    max_limit = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        """Model configuration."""

        managed = False
