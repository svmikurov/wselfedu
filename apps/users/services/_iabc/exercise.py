"""Defines exercise service."""

import uuid
from abc import ABC, abstractmethod
from typing import Protocol

from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from typing_extensions import override

from apps.users.models import CustomUser


class IBalanceService(Protocol):
    """Protocol for balance service interface."""

    @transaction.atomic
    def reward_user(
        self,
        task_uid: uuid.UUID,
        user: CustomUser,
        reward: int,
    ) -> None:
        """Add reward for task."""

    def get_balance(
        self,
        user: CustomUser | AnonymousUser,
    ) -> int | None:
        """Get user balance."""


class BalanceServiceABC(ABC, IBalanceService):
    """Abstract base class fpr service for balance operations."""

    @abstractmethod
    @transaction.atomic
    @override
    def reward_user(
        self,
        task_uid: uuid.UUID,
        user: CustomUser,
        reward: int,
    ) -> None:
        """Add reward for task."""

    @abstractmethod
    @override
    def get_balance(
        self,
        user: CustomUser | AnonymousUser,
    ) -> int | None:
        """Get user balance."""
