"""Defines main DI container."""

from dependency_injector import containers, providers

from src.apps.mathem.di_container import MathContainer


class MainContainer(containers.DeclarativeContainer):
    """Main DI container."""

    math_container = providers.Container(
        MathContainer,
    )

    # API
    math_exercise = math_container.exercise
