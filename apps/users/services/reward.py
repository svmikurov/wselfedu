"""Student reward service."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from django.db import transaction
from django.db.models import F

from apps.users.models import Balance, Transaction

from .abstract import AbstractRewardService

if TYPE_CHECKING:
    from apps.users.domains.dto import RewardDTO


__all__ = ('RewardService',)


class RewardService(AbstractRewardService):
    """Exercise reward service."""

    @override
    def increment(self, reward: RewardDTO) -> None:
        """Add reward."""
        with transaction.atomic():
            Balance.objects.update_or_create(
                user=reward.student,
                defaults={
                    'total': F('total') + reward.amount,
                },
                create_defaults={
                    'user': reward.student,
                    'total': reward.amount,
                },
            )
            Transaction.objects.create(
                user=reward.student,
                amount=reward.amount,
                type=Transaction.Operation.REWARD,
            )
