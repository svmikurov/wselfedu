"""Language discipline use case DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    DependenciesContainer,
    Dependency,
    Factory,
)

from apps.core.use_cases.exercise.resource import ExerciseCreateUseCase
from apps.lang.repositories.exercise.parameters.fetch import (
    ExerciseParametersRepository,
)


class UseCaseContainer(DeclarativeContainer):
    """Language discipline use case DI container."""

    # =============================================
    # External dependencies
    # ---------------------------------------------
    storage = Dependency()  # type: ignore[var-annotated]

    exercise_services = DependenciesContainer()
    milestone_services = DependenciesContainer()

    # =============================================
    # Translation exercise
    # ---------------------------------------------
    # Create translation test exercise use case
    start_regular_translation_test = Factory(
        ExerciseCreateUseCase,
        store_prefix='regular_translation_test',
        storage=storage,
        repository=Factory(
            ExerciseParametersRepository,
            manager=...,
        ),
        service=exercise_services.create_regular_translation_test,
        dto_factory=...,
    )
