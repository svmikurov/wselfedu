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
from contracts.schemas.domain.exercise.params import (
    ExerciseParametersDTO,
    TestExerciseConfigDTO,
)


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

    translation_presentation_resolver = Factory(
        ExerciseConfigurationResolver,
        exercise_type=ExerciseKind.PRESENTATION,
        parameters_repository=repositories.translation_parameters,
        default=None,
        name='Translation presentation configuration resolver',
        auditor=auditor,
    )
    # HACK: Implement default exercise parameters fetch
    translation_test_resolver = Factory(
        ExerciseConfigurationResolver,
        exercise_type=ExerciseKind.TEST,
        parameters_repository=repositories.translation_parameters,
        default=ExerciseParametersDTO(
            settings=TestExerciseConfigDTO(
                option_count=7,
            ),
        ),
        name='Translation test configuration resolver',
        auditor=auditor,
    )
