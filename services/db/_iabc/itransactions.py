"""Defines protocol and abc for points balance transaction service."""

from decimal import Decimal
from typing import Protocol

from wse_exercises import TaskT

from apps.users.models import CustomUser
from managers import (
    BalanceManagerT_co,
    TransactionManagerT_co,
    UserManagerT_co,
)


class ITransactionService(
    Protocol[
        BalanceManagerT_co,
        TransactionManagerT_co,
        UserManagerT_co,
    ],
):
    """Protocol for points balance transaction service interface."""

    def __init__(
        self,
        user_manager: UserManagerT_co,
        balance_manager: BalanceManagerT_co,
        transaction_manager: TransactionManagerT_co,
    ) -> None:
        """Constrict the service."""

    def add_reward(
        self,
        user: CustomUser,
        amount: Decimal,
        task: TaskT,
    ) -> None:
        """Add reward."""

    def pay_reward(
        self,
        student: CustomUser,
        mentor: CustomUser,
        amount: Decimal,
    ) -> None:
        """Pay reward."""
