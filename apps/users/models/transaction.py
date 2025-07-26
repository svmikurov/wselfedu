"""Defines balance transaction model."""

from decimal import Decimal
from typing import TypeVar

from django.core.validators import MinValueValidator
from django.db import models

TransactionT = TypeVar('TransactionT', bound='Transaction')


class Transaction(models.Model):
    """Balance transaction model."""

    class Operation(models.TextChoices):
        """Transaction type choice."""

        REWARD = 'reward'
        PAYMENT = 'payment'

    user = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='transactions',
    )
    amount = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        validators=[
            MinValueValidator(
                Decimal('0.01'),
                message='Значение должно быть > 0',
            ),
        ],
        verbose_name='Сумма транзакции',
    )
    type = models.CharField(
        max_length=30,
        choices=Operation.choices,
        verbose_name='Тип транзакции',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата транзакции',
    )

    class Meta:
        """Model configuration."""

        managed = False
        db_table = 'users"."transaction'
