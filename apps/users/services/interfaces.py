"""Defines protocols for  Users application services interface."""

import uuid
from typing import Protocol

from django.contrib.auth.models import AnonymousUser
from django.db import transaction

from apps.users.models import CustomUser


class IBalanceService(Protocol):
    """Protocol for balance service interface."""

    @staticmethod
    @transaction.atomic
    def reward_for_simple_calc_task(
        task_uid: uuid.UUID,
        user: CustomUser,
        reward: int,
    ) -> None:
        """Add reward for simple calculation task."""

    def get_balance(
        self,
        user: CustomUser | AnonymousUser,
    ) -> int | None:
        """Get user balance."""
