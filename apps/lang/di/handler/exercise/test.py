"""Test exercise request handler DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import DependenciesContainer, Factory

from apps.core.handlers import RequestHandler
from apps.core.parsers.request import NullParser
from apps.lang.handlers.types import RegularTranslationTestWebHandler


class TranslationTestContainer(DeclarativeContainer):
    """UseCase DI container."""

    validators = DependenciesContainer()
    use_cases = DependenciesContainer()
    adapters = DependenciesContainer()

    web_detail = Factory(
        RequestHandler,
        parser=Factory(NullParser),
        validator=validators.web_detail_test,
        use_case=use_cases.detail_test_loop,
        adapter=adapters.web_test,
    )
    web_regular = Factory(
        RegularTranslationTestWebHandler,
        parser=Factory(NullParser),
        validator=validators.web_regular_test,
        use_case=use_cases.regular_test_loop,
        adapter=adapters.web_test,
    )
