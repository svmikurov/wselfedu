"""Service for balance operations."""

import logging
import uuid

from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import F

from apps.math.models.points import SimplCalcReward
from apps.math.models.simple import SimpleTask

from ..models import Balance, CustomUser, Transaction
from .interfaces import IBalanceService

logger = logging.getLogger(__name__)


class BalanceService(IBalanceService):
    """Service for balance operations."""

    @staticmethod
    @transaction.atomic
    def reward_for_simple_calc_task(
        task_uid: uuid.UUID,
        user: CustomUser,
        reward: int,
    ) -> None:
        """Add reward for simple calculation task."""
        if reward <= 0:
            logger.warning(f'Reward must be positive, got {reward}')
            return

        task = SimpleTask.objects.get(uid=task_uid)

        task_reward = SimplCalcReward.objects.create(
            task=task,
            reward=reward,
        )

        user_balance, _ = Balance.objects.get_or_create(user=user)

        content_type = ContentType.objects.get_for_model(SimplCalcReward)

        Transaction.objects.create(
            user_balance=user_balance,
            content_type=content_type,
            object_id=task_reward.id,
            operation_type=Transaction.Operation.REWARD,
            amount=reward,
        )

        Balance.objects.select_for_update().filter(
            user=user,
        ).update(
            points=F('points') + reward,
        )

    def get_balance(
        self,
        user: CustomUser | AnonymousUser,
    ) -> int | None:
        """Get user balance."""
        if not user.is_authenticated:
            return None

        user_balance, _ = Balance.objects.get_or_create(user=user)
        return user_balance.points
