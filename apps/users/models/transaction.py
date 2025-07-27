"""Defines transaction model that combined all transaction model."""

from django.db import models

from apps.main.models import BaseTransaction
from apps.users.models import CustomUser


class Transaction(BaseTransaction):
    """Combined transaction model."""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='transactions',
    )

    class Meta:
        """Model configuration."""

        managed = False
        db_table = 'main"."transaction'
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
