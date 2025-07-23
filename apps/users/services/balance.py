"""Defines user balance service."""

import logging
import uuid
from typing import Generic

from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.db.models import F
from typing_extensions import override

from apps.main.models.base.reward import BaseRewardT, BaseTaskT

from ..models import CustomUser
from ..models.balance import BalanceT
from ..models.transaction import TransactionT
from ._iabc.exercise import BalanceServiceABC

logger = logging.getLogger(__name__)


class BalanceService(
    BalanceServiceABC,
    Generic[BaseTaskT, BaseRewardT, BalanceT],
):
    """Service for balance operations."""

    def __init__(
        self,
        task_manager: models.Manager[BaseTaskT],
        reward_manager: models.Manager[BaseRewardT],
        balance_manager: models.Manager[BalanceT],
        transaction_manager: models.Manager[TransactionT],
    ) -> None:
        """Construct the service."""
        self._task_manager = task_manager
        self._reward_manager = reward_manager
        self._balance_manager = balance_manager
        self._transaction_manager = transaction_manager

    @transaction.atomic
    @override
    def reward_user(
        self,
        task_uid: uuid.UUID,
        user: CustomUser,
        reward: int,
    ) -> None:
        """Add reward for task."""
        if reward <= 0:
            logger.warning(f'Reward must be positive, got {reward}')
            return

        #
        operation_type = self._transaction_manager.model.Operation.REWARD

        # Get reward task
        task = self._task_manager.get(uid=task_uid)

        # Create an award record
        task_reward = self._reward_manager.create(
            task=task,
            reward=reward,
        )

        # Getting/creating a user's balance
        user_balance, _ = self._balance_manager.get_or_create(user=user)

        # Increase balance
        user_balance.update(  # type: ignore[attr-defined]
            amount=F('amount') + reward,
        )

        # Getting a ContentType for a reward
        content_type = ContentType.objects.get_for_model(
            self._reward_manager.model
        )

        # Create transaction
        self._transaction_manager.create(
            user_balance=user_balance,
            content_type=content_type,
            object_id=task_reward.id,  # type: ignore[attr-defined]
            operation_type=operation_type,
            amount=reward,
        )

    @override
    def get_balance(
        self,
        user: CustomUser | AnonymousUser,
    ) -> int | None:
        """Get user balance."""
        if not user.is_authenticated:
            return None

        user_balance, _ = self._balance_manager.get_or_create(user=user)
        return user_balance.amount
