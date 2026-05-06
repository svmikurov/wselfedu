"""Use case result builder DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dict, Factory

from apps.core.builders.exercise.task import (
    ExercisePresentationBuilder,
    TestExerciseTaskBuilder,
)
from apps.core.builders.null import NullSpecDtoBuilder
from contracts.enums import ExerciseStatus


class UseCaseResultBuilderContainer(DeclarativeContainer):
    """Use case result builder DI container."""

    # =============================================
    # Exercise domain result builders
    # =============================================

    _null = Factory(NullSpecDtoBuilder)  # type: ignore

    _presentation = Factory(  # type: ignore
        ExercisePresentationBuilder,
    )
    _test = Factory(  # type: ignore
        TestExerciseTaskBuilder,
    )

    # =============================================
    # Exercise domain result builder registry
    # =============================================

    presentation_registry = Dict(
        {
            ExerciseStatus.NEW_TASK: _presentation,
            ExerciseStatus.UPDATED_PROGRESS: _null,
        },
    )
    test_registry = Dict(
        {
            ExerciseStatus.NEW_TASK: _test,
            ExerciseStatus.UPDATED_PROGRESS: _null,
        },
    )
