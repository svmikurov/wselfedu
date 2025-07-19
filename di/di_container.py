"""Defines the Core dependency injection container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Container

from apps.math.di_container import MathAppContainer


class CoreContainer(DeclarativeContainer):
    """Core DI container."""

    math_container: Container[MathAppContainer] = Container(
        MathAppContainer,
    )
