"""Main dependency injection container."""

from dependency_injector.containers import (
    DeclarativeContainer,
    WiringConfiguration,
)
from dependency_injector.providers import (
    Container,
    Dependency,
    Factory,
)

from wse.application.use_case import CreateTaskUseCase
from wse.domain.services.task import CreateTaskService
from wse.infrastructure.in_memory_repository import (
    InMemoryCandidatesRepository,
)


class DomainContainer(DeclarativeContainer):
    """Domain layer service the dependency injection container."""

    create_task = Factory(CreateTaskService)


class InfrastructureContainer(DeclarativeContainer):
    """Infrastructure layer the dependency injection container."""

    in_memory_candidates = Factory(InMemoryCandidatesRepository)


class ApplicationContainer(DeclarativeContainer):
    """Application layer the dependency injection container."""

    # External dependencies

    repository = Dependency()  # type: ignore[var-annotated]
    domain = Dependency()  # type: ignore[var-annotated]

    # Dependencies

    create_task_use_case = Factory(
        CreateTaskUseCase,
        repository=repository,
        domain=domain,
    )


class MainContainer(DeclarativeContainer):
    """Main dependency injection container."""

    wiring_config = WiringConfiguration(
        modules=['..entrypoints.flask_app.views']
    )

    domain = Container(DomainContainer)
    infra = Container(InfrastructureContainer)
    app = Container(
        ApplicationContainer,
        repository=infra.in_memory_candidates,
        domain=domain.create_task,
    )
