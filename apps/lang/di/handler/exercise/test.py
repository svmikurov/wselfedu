"""Test exercise request handler DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import DependenciesContainer, Factory

from apps.core.handlers import (
    RegularRequestHandler,
    ResourceRequestHandler,
)


class TranslationTestContainer(DeclarativeContainer):
    """UseCase DI container."""

    validators = DependenciesContainer()
    use_cases = DependenciesContainer()
    adapters = DependenciesContainer()

    web_detail = Factory(
        ResourceRequestHandler,
        validator=validators.web_detail_test,
        use_case=use_cases.detail_test_loop,
        adapter=adapters.web_test,
    )
    web_regular = Factory(
        RegularRequestHandler,
        validator=validators.web_regular_test,
        use_case=use_cases.regular_test_loop,
        adapter=adapters.web_test,
    )
