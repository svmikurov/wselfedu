"""Use case result builder DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dict, Factory

from apps.core.builders.exercise.task import ExercisePresentationBuilder
from apps.core.builders.null import NullSpecDtoBuilder
from contracts.enums import ExerciseStatus


class UseCaseResultBuilderContainer(DeclarativeContainer):
    """Use case result builder DI container."""

    # =============================================
    # Exercise domain result builders
    # =============================================

    presentation = Factory(  # type: ignore
        ExercisePresentationBuilder,
    )
    null_builder = Factory(NullSpecDtoBuilder)  # type: ignore

    # =============================================
    # Exercise domain result builder registry
    # =============================================

    presentation_registry = Dict(
        {
            ExerciseStatus.NEW_TASK: presentation,
            ExerciseStatus.UPDATED_PROGRESS: null_builder,
        },
    )
