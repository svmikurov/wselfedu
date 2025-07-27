"""Defines reward transaction proxy model on Lang exercise."""

from django.db import models

from apps.main.models import BaseTransaction
from apps.users.models import CustomUser


class LangTransaction(BaseTransaction):
    """Reward transaction proxy model on Lang exercise."""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='lang_transactions',
    )

    class Meta:
        """Model configuration."""

        managed = False
        db_table = 'lang"."transaction'
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
