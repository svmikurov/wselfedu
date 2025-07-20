"""Definer balance manager."""

from decimal import Decimal

from django.db import models, transaction

from apps.users.models import Balance
from services.storage import ICacheUserIDClient


class BalanceManager(models.Manager[Balance]):
    """Balance model manager."""

    CACHE_PREFIX = 'balance'
    CACHE_TTL = 6000

    def __init__(
        self,
        cache: ICacheUserIDClient,
    ) -> None:
        """Construct the manager."""
        super().__init__()
        self._cache = cache

    @transaction.atomic
    def update_amount(
        self,
        user_id: int,
        amount: Decimal,
    ) -> bool:
        """Update balance with daily limit."""
        updated = (
            self
            .filter(user_id=user_id)
            .update(amount=models.F('amount') + amount)
        )  # fmt: skip
        return updated == 1

    def get_balance(
        self,
        user_id: int,
    ) -> Decimal | None:
        """Get user balance."""
        balance = self._cache.get(user_id, prefix=self.CACHE_PREFIX)

        if isinstance(balance, Decimal):
            return balance

        elif balance is None:
            balance = self._get_uncached_balance(user_id)
            self._cache_balance(user_id, balance)
            return balance

        else:
            raise TypeError(
                f'Expected `Decimal` type balance, got {type(balance)}'
            )

    def _get_uncached_balance(self, user_id: int) -> Decimal:
        balance = (
            self
            .filter(user_id=user_id)
            .values_list('amount', flat=True)
            .first()
        )  # fmt: skip

        if not isinstance(balance, Decimal):
            raise TypeError(
                f'Expected `Decimal` type balance, got {type(balance)}'
            )

        return Decimal(balance)

    def _cache_balance(self, user_id: int, balance: Decimal) -> None:
        self._cache.set(balance, user_id, self.CACHE_PREFIX, self.CACHE_TTL)
