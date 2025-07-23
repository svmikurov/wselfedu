"""Defines transaction model manager."""

from typing import Any, Iterable

from django.db import models, transaction

from apps.users.models import Transaction


class TransactionManager(models.Manager[Transaction]):
    """Transaction model manager."""

    BATCH_SIZE = 500

    @transaction.atomic
    def bulk_create_optimized(self, transactions: Iterable[Any]) -> list[Any]:
        """Create transaction."""
        return self.bulk_create(transactions, batch_size=self.BATCH_SIZE)
