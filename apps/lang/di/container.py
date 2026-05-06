"""Language discipline DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    Container,
    DependenciesContainer,
    Dependency,
)

from .config.container import LanguageConfigurationContainer
from .handler.web.container import WebHandlerContainer
from .repository.repository import LanguageRepositoryContainer
from .service.container import ServiceContainer
from .use_case.container import LangUseCaseContainer
from .validator.container import LangValidatorContainer


class LanguageContainer(DeclarativeContainer):
    """Language discipline DI container."""

    # ===========================================
    # External dependencies
    # ===========================================
    spec_factories = DependenciesContainer()
    domains = DependenciesContainer()
    use_case_result_builders = DependenciesContainer()
    response_adapters = DependenciesContainer()

    storage = Dependency()  # type: ignore[var-annotated]
    user_command_storage = Dependency()  # type: ignore[var-annotated]

    auditor = Dependency()  # type: ignore[var-annotated]

    # ===========================================
    # Internal dependencies
    # ===========================================

    repositories = Container(
        LanguageRepositoryContainer,
        storage=storage,
        auditor=auditor,
    )
    lang_configurations = Container(
        LanguageConfigurationContainer,
        repositories=repositories,
        auditor=auditor,
    )
    validators = Container(
        LangValidatorContainer,
    )
    services = Container(
        ServiceContainer,
        domains=domains,
        repositories=repositories,
        auditor=auditor,
    )
    use_cases = Container(
        LangUseCaseContainer,
        lang_config=lang_configurations,
        repositories=repositories,
        spec_factories=spec_factories,
        services=services,
        use_case_result_builders=use_case_result_builders,
        user_command_storage=user_command_storage,
        auditor=auditor,
    )
    handlers = Container(
        WebHandlerContainer,
        validators=validators,
        use_cases=use_cases,
        response_adapters=response_adapters,
        user_command_storage=user_command_storage,
        auditor=auditor,
    )
