"""Defines transaction model."""

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Transaction(models.Model):
    """Balance transaction model."""

    class Operation(models.TextChoices):
        """Transaction type choice."""

        REWARD = 'reward'
        PAYMENT = 'payment'

    user = models.ForeignKey(
        'users.Person',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
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
        verbose_name='Сумма',
    )
    type = models.CharField(
        max_length=30,
        choices=Operation.choices,
        verbose_name='Тип',
        help_text='Transaction type (reward/payment)',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

        db_table = 'users_balance_transaction'
