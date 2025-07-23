"""Defines protocol and abc for balance model manager."""

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Protocol, TypeVar

from django.db import models

from apps.users.models import Balance, CustomUser

BalanceM_co = TypeVar('BalanceM_co', bound=Balance, covariant=True)
UserT_contr = TypeVar('UserT_contr', bound=CustomUser, contravariant=True)
BalanceManagerT_co = TypeVar(
    'BalanceManagerT_co', bound='IBalanceManager[Balance]', covariant=True
)


class IBalanceManager(
    Protocol[BalanceM_co],
):
    """Protocol for balance manger interface."""

    def add_reward(
        self,
        reward: Decimal,
        user: UserT_contr,
    ) -> None:
        """Add reward into balance."""


class BalanceManagerFeaturesABC(
    ABC,
    IBalanceManager[BalanceM_co],
):
    """ABC for balance model manager features."""

    @abstractmethod
    def add_reward(
        self,
        reward: Decimal,
        user: UserT_contr,
    ) -> None:
        """Add reward into balance."""


class BaseBalanceManager(
    models.Manager[BalanceM_co],
    BalanceManagerFeaturesABC[BalanceM_co],
    ABC,
):
    """Base balance model manager."""
