"""Defines reward transaction proxy model on Lang exercise."""

from apps.core.models import BaseTransaction


class LangTransaction(BaseTransaction):
    """Reward transaction proxy model on Lang exercise."""

    class Meta:
        """Model configuration."""

        managed = False
        db_table = 'lang"."transaction'
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
