"""language app's configuration DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    DependenciesContainer,
    Dependency,
    Factory,
)

from apps.core.resolvers.exercise.config_resolver import (
    ExerciseConfigurationResolver,
)
from contracts.enums.exercise import ExerciseKind


class LanguageConfigurationContainer(DeclarativeContainer):
    """language app's configuration DI container."""

    # =============================================
    # External dependencies
    # =============================================

    repositories = DependenciesContainer()

    auditor = Dependency()  # type: ignore[var-annotated]

    # =============================================
    # Internal dependencies
    # =============================================

    translation_exercise_config_resolver = Factory(
        ExerciseConfigurationResolver,
        exercise_type=ExerciseKind.PRESENTATION,
        parameters_repository=repositories.translation_parameters,
        default=None,
        name='Exercise configuration resolver',
        auditor=auditor,
    )
