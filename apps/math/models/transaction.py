"""Defines reward transaction proxy model on math exercise."""

from apps.users.models import Transaction


class MathTransaction(Transaction):
    """Reward transaction proxy model on math exercise."""

    class Meta:
        """Model configuration."""

        proxy = True
        db_table = 'math"."transaction'
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
