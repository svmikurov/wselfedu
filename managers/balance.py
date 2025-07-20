"""Definer balance manager."""

from decimal import Decimal
from functools import lru_cache

from django.db import models, transaction


class BalanceManager(models.Manager):
    """Balance model manager."""

    @transaction.atomic
    def update(
        self,
        user_id: int,
        amount: Decimal,
    ) -> bool:
        """Update balance with daily limit."""
        return (
            self
            .filter(user_id=user_id)
            .update(amount=models.F('amount') + amount)
        ) > 0

    @lru_cache(maxsize=1000)
    def get_balance(
        self,
        user_id: int,
    ) -> Decimal | None:
        """Get user balance."""
        return (
            self
            .filter(user_id=user_id)
            .values_list('amount', flat=True)
            .first()
        )
