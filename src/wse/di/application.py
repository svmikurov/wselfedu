"""Application DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Container, Factory

from wse.application import use_cases

from . import domain, infrastructure


class ApplicationContainer(DeclarativeContainer):
    """Application DI container."""

    ###############################################
    # External dependency containers
    ###############################################

    services = Container(domain.DomainContainer)
    repositories = Container(infrastructure.RepositoryContainer)

    ###############################################
    # Use cases
    ###############################################

    create_testing = Factory(
        use_cases.CreateTestingUseCase,
        learnables_repo=repositories.learnable,
        task_repo=repositories.task,
        service=services.create_testing,
    )
    check_testing = Factory(
        use_cases.CheckTestingUseCase,
        repo=repositories.task,
        service=services.check_testing,
    )
