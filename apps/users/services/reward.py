"""Student reward service."""

from typing import override

from django.db import transaction
from django.db.models import F

from apps.users.domains.dto import RewardDTO
from apps.users.models import Balance, Transaction
from utils import decorators

from .abstract import AbstractRewardService

__all__ = ('RewardService',)


class RewardService(AbstractRewardService):
    """Exercise reward service."""

    @override
    @decorators.log_unimplemented_call
    def increment(self, reward: RewardDTO) -> None:
        """Add reward."""
        with transaction.atomic():
            Balance.objects.update_or_create(
                pk=reward.student_pk,
                defaults={'total': F('total') + reward.amount},
                create_defaults={
                    'total': reward.amount,
                    'user_id': reward.student_pk,
                },
            )
            Transaction.objects.create(
                user_id=reward.student_pk,
                amount=reward.amount,
                type=Transaction.Operation.REWARD,
            )
