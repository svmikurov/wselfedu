"""Defines user reward models."""

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Balance(models.Model):
    """User points balance."""

    user = models.ForeignKey(
        'CustomUser', on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    points = models.PositiveSmallIntegerField(
        default=0, verbose_name='Всего очков'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлен'
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    def __str__(self) -> str:
        """Return the text representation of object."""
        return f'{self.user}`s: {self.points} points'

    def __repr__(self) -> str:
        """Return the representation of object."""
        return f'<{self.user}: {self.points} points>'


class Transaction(models.Model):
    """Points transaction."""

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
