"""Language app service's DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    DependenciesContainer,
    Dict,
    Factory,
)

from apps.core import services
from apps.core.builders.exercise.case import ExerciseCaseBuilder
from contracts.enums.exercise import ExerciseAction


class ServiceContainer(DeclarativeContainer):
    """Service DI container."""

    # =============================================
    # External dependencies
    # =============================================

    domains = DependenciesContainer()
    repositories = DependenciesContainer()

    # =============================================
    # Internal dependencies
    # =============================================

    exercise_case_builder = Factory(ExerciseCaseBuilder)  # type: ignore

    # =============================================
    # Exercise's services
    # =============================================

    # Create

    create_translation_presentation = Factory(
        services.CreateExerciseService,
        candidates_repository=repositories.translation_candidates,
        domain=domains.presentation,
        builder=exercise_case_builder,
    )
    create_translation_test = Factory(
        services.CreateExerciseService,
        candidates_repository=repositories.translation_candidates,
        domain=domains.test,
        builder=exercise_case_builder,
    )

    # Progress

    translation_progress = Factory(
        services.UpdateProgressService,
        repository=repositories.regular_translation_progress,
    )

    # =============================================
    # Exercise service's registries
    # =============================================

    regular_translation_presentation_registry = Dict(
        {
            ExerciseAction.CREATE_TASK: create_translation_presentation,
            ExerciseAction.UPDATE_PROGRESS: translation_progress,
        },
    )
    regular_translation_test_registry = Dict(
        {
            ExerciseAction.CREATE_TASK: create_translation_test,
            ExerciseAction.UPDATE_PROGRESS: translation_progress,
        },
    )
