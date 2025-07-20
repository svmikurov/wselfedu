"""Defines user reward models."""

from typing import TypeVar

from django.db import models

BalanceT = TypeVar('BalanceT', bound='Balance')


class Balance(models.Model):
    """User points balance."""

    user = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    points = models.PositiveSmallIntegerField(
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
        return f'{self.user}`s: {self.points} points'

    def __repr__(self) -> str:
        """Return the representation of object."""
        return f'<{self.user}: {self.points} points>'
