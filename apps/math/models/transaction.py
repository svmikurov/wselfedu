"""Defines reward transaction proxy model on math exercise."""

from django.db import models

from apps.main.models import BaseTransaction
from apps.users.models import CustomUser


class MathTransaction(BaseTransaction):
    """Reward transaction proxy model on math exercise."""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='math_transactions',
    )

    class Meta:
        """Model configuration."""

        managed = False
        db_table = 'math"."transaction'
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
