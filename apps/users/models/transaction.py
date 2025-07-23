"""Defines balance transaction model."""

from decimal import Decimal
from typing import TypeVar

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator
from django.db import models

TransactionT = TypeVar('TransactionT', bound='Transaction')


class Transaction(models.Model):
    """Balance transaction model."""

    class Operation(models.TextChoices):
        """Transaction type choice."""

        REWARD = 'reward'
        PAYMENT = 'payment'

    balance = models.ForeignKey(
        'Balance',
        on_delete=models.CASCADE,
        verbose_name='Баланс',
        related_name='transactions',
    )

    # Generic foreign key
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    object_uid = models.UUIDField()
    content_object = GenericForeignKey(
        'content_type',
        'object_uid',
    )

    operation_type = models.CharField(
        max_length=20,
        choices=Operation.choices,
    )
    amount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(
                Decimal('0.01'),
                message='Значение должно быть > 0',
            ),
        ],
        verbose_name='Сумма транзакции',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )

    class Meta:
        """Configure the model."""

        indexes = [models.Index(fields=['content_type', 'object_uid'])]
