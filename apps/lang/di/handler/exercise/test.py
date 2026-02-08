"""Test exercise request handler DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import DependenciesContainer, Factory

from apps.core.handlers import (
    DetailRequestHandler,
    RegularRequestHandler,
)


class TranslationTestContainer(DeclarativeContainer):
    """UseCase DI container."""

    validators = DependenciesContainer()
    services = DependenciesContainer()
    adapters = DependenciesContainer()

    web_detail = Factory(
        DetailRequestHandler,
        validator=validators.web_detail_test,
        service=services.detail_test_loop,
        adapter=adapters.web_test,
    )
    web_regular = Factory(
        RegularRequestHandler,
        validator=validators.web_regular_test,
        service=services.regular_test_loop,
        adapter=adapters.web_test,
    )
