"""Main dependency injection container."""

from dependency_injector.containers import (
    DeclarativeContainer,
    WiringConfiguration,
)
from dependency_injector.providers import (
    Container,
    DependenciesContainer,
    Dependency,
    Factory,
)

from wse.application.use_case import CreateTaskUseCase
from wse.domain.services.task import (
    CreatePresentationService,
    CreateTestingService,
)
from wse.infrastructure.in_memory_repository import (
    InMemoryCandidatesRepository,
)


class DomainContainer(DeclarativeContainer):
    """Domain layer service the dependency injection container."""

    presentation = Factory(CreatePresentationService)
    testing = Factory(CreateTestingService)


class InfrastructureContainer(DeclarativeContainer):
    """Infrastructure layer the dependency injection container."""

    in_memory_candidates = Factory(InMemoryCandidatesRepository)


class ApplicationContainer(DeclarativeContainer):
    """Application layer the dependency injection container."""

    # External dependencies

    repository = Dependency()  # type: ignore[var-annotated]
    domains = DependenciesContainer()

    # Dependencies

    create_presentation_use_case = Factory(
        CreateTaskUseCase,
        repository=repository,
        domain=domains.presentation,
    )


class MainContainer(DeclarativeContainer):
    """Main dependency injection container."""

    wiring_config = WiringConfiguration(
        modules=['..entrypoints.flask_app.views']
    )

    domains = Container(DomainContainer)
    infrastructures = Container(InfrastructureContainer)
    applications = Container(
        ApplicationContainer,
        repository=infrastructures.in_memory_candidates,
        domains=domains,
    )
