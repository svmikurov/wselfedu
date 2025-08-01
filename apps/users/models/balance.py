"""Defines user reward models."""

from django.db import models


class Balance(models.Model):
    """User points balance."""

    user = models.OneToOneField(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='balance',
        verbose_name='Пользователь',
    )
    total = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        verbose_name='Баланс',
    )
    created_at = models.DateTimeField(
        blank=True,
        auto_now_add=True,
        verbose_name='Добавлен',
    )
    updated_at = models.DateTimeField(
        blank=True,
        auto_now=True,
        verbose_name='Обновлен',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Баланс'
        verbose_name_plural = 'Баланс'

    def __str__(self) -> str:
        """Return the text representation of object."""
        return f'Баланс {self.user}: {self.total}'

    def __repr__(self) -> str:
        """Return the representation of object."""
        return f'<{self.user}: {self.total}>'
