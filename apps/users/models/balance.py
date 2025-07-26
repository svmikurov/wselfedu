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
    total = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        verbose_name='Всего очков',
    )
    created_at = models.DateTimeField(
        blank=True,
        verbose_name='Добавлен',
    )
    updated_at = models.DateTimeField(blank=True, verbose_name='Обновлен')

    class Meta:
        """Model configuration."""

        managed = False
        db_table = 'users"."balance'

    def __str__(self) -> str:
        """Return the text representation of object."""
        return f'{self.user}`s: {self.total} points'

    def __repr__(self) -> str:
        """Return the representation of object."""
        return f'<{self.user}: {self.total} points>'
