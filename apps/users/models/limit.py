"""Defines reward limits."""

from django.db import models

from apps.users.models import CustomUser


class RewardLimit(models.Model):
    """Reward limits."""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )
    limit = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
