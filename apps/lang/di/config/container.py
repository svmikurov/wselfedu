"""Configuration dependency."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    DependenciesContainer,
    Factory,
)

from apps.core.domains.exercise.enums import ExerciseTypeEnum
from apps.core.use_cases.exercise.perform.config_resolver import (
    ExerciseConfigurationResolver,
)


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
        exercise_type=ExerciseTypeEnum.PRESENTATION,
        parameters_repository=repositories.translation_parameters,
        default=None,
    )
