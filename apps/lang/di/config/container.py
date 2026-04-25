"""Configuration dependency."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    DependenciesContainer,
    Factory,
)

from apps.core.resolvers.exercise.config_resolver import (
    ExerciseConfigurationResolver,
)
from interfaces.enums.exercise import ExerciseKind


class ConfigurationContainer(DeclarativeContainer):
    """Configuration DI container."""

    # =============================================
    # External dependencies
    # =============================================

    repositories = DependenciesContainer()

    # =============================================
    # Internal dependencies
    # =============================================

    exercise_config_resolver = Factory(
        ExerciseConfigurationResolver,
        exercise_type=ExerciseKind.PRESENTATION,
        parameters_repository=repositories.translation_parameters,
        default=None,
    )
