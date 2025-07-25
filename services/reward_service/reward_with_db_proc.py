"""Defines reward service uses Postgres procedures."""

from decimal import Decimal
from functools import lru_cache
from typing import Type

from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction

from apps.users.models import CustomUser, Transaction


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
        # Update the transaction

        Transaction.objects.create(
            amount=amount,
            operation_type=Transaction.Operation.REWARD,
            object_uid=related_object.uid,  # type: ignore[attr-defined]
        )

    @staticmethod
    @lru_cache(maxsize=32)
    def _get_content_type(model: Type[models.Model]) -> ContentType:
        """Cache to get ContentType."""
        return ContentType.objects.get_for_model(model)
