"""Defines balance transaction model."""

from typing import TypeVar

from django.contrib.contenttypes.fields import (
    GenericForeignKey,
)
from django.contrib.contenttypes.models import ContentType
from django.db import models

TransactionT = TypeVar('TransactionT', bound='Transaction')


class Transaction(models.Model):
    """Balance transaction model."""

    class Operation(models.TextChoices):
        """Transaction type choice."""

        REWARD = 'reward'
        PAYMENT = 'payment'

    user_balance = models.ForeignKey(
        'Balance',
        on_delete=models.CASCADE,
        verbose_name='Баланс',
    )

    # Generic foreign key
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="transactions",  # Added for documentation
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        'content_type',
        'object_id',
    )

    operation_type = models.CharField(
        max_length=20,
        choices=Operation.choices,
    )
    amount = models.PositiveSmallIntegerField(verbose_name='Очки')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )

    class Meta:
        """Configure the model."""

        indexes = [models.Index(fields=['content_type', 'object_id'])]
