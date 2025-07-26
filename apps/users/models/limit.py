"""Defines reward limits."""

from django.db import models


class RewardLimit(models.Model):
    """Reward limits."""

    user = models.ForeignKey(
        'CustomUser', on_delete=models.CASCADE, verbose_name='Обучающийся'
    )
    # TODO: Add calculation for remainder field
    #  remainder = limit - sum(main.transaction for today)
    remainder = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Остаток лимита',
    )
    limit = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Дневной лимит',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Лимит ежедневного вознаграждения'
