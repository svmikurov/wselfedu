"""Defines reward service."""

from decimal import Decimal
from functools import lru_cache
from typing import Type

from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.utils import timezone

from apps.users.models import Balance, CustomUser, Transaction


class RewardService:
    """Reward service."""

    @transaction.atomic
    def add_reward(
        self,
        user: CustomUser,
        amount: Decimal,
        related_model: Type[models.Model],
        related_object: models.Model,
    ) -> None:
        """Add daily reward for task."""
        # Update the balance

        balance, is_created = (
            Balance.objects.only('id')
            .select_for_update()
            .get_or_create(
                user=user,
                defaults={'amount': amount},
            )
        )
        if not is_created:
            (
                Balance.objects.filter(id=balance.id).update(
                    amount=models.F('amount') + amount,
                    updated_at=timezone.now(),
                )
            )

        content_type = self._get_content_type(related_model)

        # Update the transaction

        Transaction.objects.create(
            balance=balance,
            amount=amount,
            operation_type=Transaction.Operation.REWARD,
            content_type=content_type,
            object_uid=related_object.uid,  # type: ignore[attr-defined]
        )

    @staticmethod
    @lru_cache(maxsize=32)
    def _get_content_type(model: Type[models.Model]) -> ContentType:
        """Cache to get ContentType."""
        return ContentType.objects.get_for_model(model)
