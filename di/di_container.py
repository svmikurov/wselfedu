"""Defines the Core dependency injection container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Container

from apps.core.di_container import CoreContainer
from apps.math.di_container import MathAppContainer


class MainContainer(DeclarativeContainer):
    """Main DI container."""

    core_container: Container[CoreContainer] = Container(
        CoreContainer,
    )
    math_container: Container[MathAppContainer] = Container(
        MathAppContainer,
        task_storage=core_container.task_storage,
    )
