"""Defines main DI container."""

from dependency_injector import containers, providers

from apps.mathem.di_container import MathContainer


class MainContainer(containers.DeclarativeContainer):
    """Main DI container."""

    math = providers.Container(
        MathContainer,
    )
