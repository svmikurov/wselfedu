"""Defines optimal balance service."""

from dataclasses import dataclass
from decimal import Decimal

from django.db import transaction

from managers.balance import BalanceManager
from managers.basis import TaskManager
from managers.transaction import TransactionManager
from managers.user import UserManager


@dataclass
class BalanceUpdateResult:
    """Result of balance update DTO."""

    success: bool
    new_balance: Decimal | None
    transaction_id: int | None


class BalanceService:
    """Balance service."""

    def __init__(
        self,
        balance_manager: BalanceManager,
        transaction_manager: TransactionManager,
        user_manager: UserManager,
        task_manager: TaskManager,
    ) -> None:
        """Construct the service."""
        self._balance = balance_manager
        self._transactions = transaction_manager
        self._users = user_manager
        self._tasks = task_manager

    @transaction.atomic
    def update_balance(
        self, user_id: int, amount: Decimal, task_uid: int, comment: str = ''
    ) -> BalanceUpdateResult:
        """Update balance."""
        try:
            if not self._validate_operation(user_id, task_uid):
                return BalanceUpdateResult(False, None, None)

            success = self._balance.update_amount(user_id, amount)
            if not success:
                return BalanceUpdateResult(False, None, None)

            new_balance = self._balance.get_balance(user_id)
            # TODO: Fix Transaction model or manager
            transaction = self._transactions.create(  # type: ignore
                user_id=user_id,
                amount=amount,
                balance_after=new_balance,
                task_uid=task_uid,
                comment=comment,
            )

            return BalanceUpdateResult(True, new_balance, transaction.id)

        except Exception:
            return BalanceUpdateResult(False, None, None)

    @staticmethod
    def _validate_operation(user_id: int, task_uid: int) -> bool:
        return True
