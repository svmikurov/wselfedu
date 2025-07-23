"""Defines DI-container for database services."""

from dependency_injector import containers, providers

from apps.users.services.balance import BalanceService


class DBServicesContainer(containers.DeclarativeContainer):
    """DI-container for database services."""

    managers = providers.DependenciesContainer()

    balance_service = providers.Factory(
        BalanceService,
        balance_manager=managers.balance_manager,
        transaction_manager=managers.transaction_manager,
        user_manager=managers.user_manager,
        basis_manager=managers.basis_manager,
    )
