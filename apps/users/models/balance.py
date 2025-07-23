"""Defines user reward models."""

from typing import TypeVar

from django.db import models

BalanceT = TypeVar('BalanceT', bound='Balance')


class Balance(models.Model):
    """User points balance."""

    user = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='balance',
        verbose_name='Пользователь',
    )
    amount = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Всего очков',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлен',
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    def __str__(self) -> str:
        """Return the text representation of object."""
        return f'{self.user}`s: {self.amount} points'

    def __repr__(self) -> str:
        """Return the representation of object."""
        return f'<{self.user}: {self.amount} points>'
