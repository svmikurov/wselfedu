"""Defines reward transaction proxy model on Lang exercise."""

from apps.users.models import Transaction


class LangTransaction(Transaction):
    """Reward transaction proxy model on Lang exercise."""

    class Meta:
        """Model configuration."""

        proxy = True
        db_table = 'lang"."transaction'
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
