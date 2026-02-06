"""Language discipline Exercises DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Container, DependenciesContainer

from .presentation import TranslationPresentationContainer
from .test import TranslationTestContainer


class ExerciseHandlerContainer(DeclarativeContainer):
    """Language discipline exercise handler DI container."""

    validators = DependenciesContainer()
    services = DependenciesContainer()
    adapters = DependenciesContainer()

    presentation = Container(
        TranslationPresentationContainer,
        validators=validators,
        services=services,
        adapters=adapters,
    )

    test_exercise = Container(
        TranslationTestContainer,
        validators=validators,
        services=services,
        adapters=adapters,
    )
