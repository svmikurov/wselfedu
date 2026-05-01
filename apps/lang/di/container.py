"""Language discipline DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    Container,
    DependenciesContainer,
    Dependency,
)

from .config.container import ConfigurationContainer
from .handler.web.container import WebHandlerContainer
from .repository.repository import RepositoryContainer
from .service.container import ServiceContainer
from .use_case.container import UseCaseContainer


class LanguageContainer(DeclarativeContainer):
    """Language discipline DI container."""

    # ===========================================
    # External dependencies
    # ===========================================
    storage = Dependency()  # type: ignore[var-annotated]
    user_command_storage = Dependency()  # type: ignore[var-annotated]
    auditor = Dependency()  # type: ignore[var-annotated]

    domains = DependenciesContainer()

    # ===========================================
    # Internal dependencies
    # ===========================================

    repositories = Container(
        RepositoryContainer,
        storage=storage,
    )
    configurations = Container(
        ConfigurationContainer,
        repositories=repositories,
    )
    services = Container(
        ServiceContainer,
        domains=domains,
        repositories=repositories,
    )
    use_cases = Container(
        UseCaseContainer,
        configurations=configurations,
        repositories=repositories,
        services=services,
        user_command_storage=user_command_storage,
        auditor=auditor,
    )
    handlers = Container(
        WebHandlerContainer,
        use_cases=use_cases,
        user_command_storage=user_command_storage,
        auditor=auditor,
    )
