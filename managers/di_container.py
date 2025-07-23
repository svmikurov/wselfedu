"""Defines DI-container for model managers."""

from dependency_injector import containers, providers

from .balance import BalanceManager
from .basis import TaskManager
from .transaction import TransactionManager
from .user import UserManager


class ManagerContainer(containers.DeclarativeContainer):
    """DI container for model managers."""

    user_manager = providers.Singleton(
        UserManager,
    )
    balance_manager = providers.Singleton(
        BalanceManager,
        user_manager=user_manager,
    )
    transaction_manager = providers.Singleton(
        TransactionManager,
        user_manager=user_manager,
    )
    basis_manager = providers.Singleton(
        TaskManager,
    )
