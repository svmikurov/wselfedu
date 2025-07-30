"""Defines reward transaction proxy model on math exercise."""

from apps.core.models import BaseTransaction


class MathTransaction(BaseTransaction):
    """Reward transaction proxy model on math exercise."""

    class Meta:
        """Model configuration."""

        managed = False
        db_table = 'math"."transaction'
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
