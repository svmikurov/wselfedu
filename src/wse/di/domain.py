"""Domain DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory

from wse.domain import services


class DomainContainer(DeclarativeContainer):
    """Domain DI container."""

    create_testing = Factory(services.CreateTestingService)
    check_testing = Factory(services.CheckTestingService)
