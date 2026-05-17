"""Use case result builder DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dict, Factory

from kernel.builder.null import NullSpecDtoBuilder
from kernel.builder.use_case.exercise import ExerciseUseCaseResultBuilder
from ports.contract.enums import ExerciseStatus


class UseCaseResultBuilderContainer(DeclarativeContainer):
    """Use case result builder DI container."""

    # =============================================
    # Exercise domain result builders
    # =============================================

    _task = Factory(ExerciseUseCaseResultBuilder)  # type: ignore
    _null = Factory(NullSpecDtoBuilder)  # type: ignore

    # =============================================
    # Exercise domain result builder registry
    # =============================================

    # REVIEW: Is necessary the use case result registry?

    presentation_registry = Dict(
        {
            ExerciseStatus.NEW_TASK: _null,
            ExerciseStatus.UPDATED_PROGRESS: _null,
        },
    )
    test_registry = Dict(
        {
            ExerciseStatus.NEW_TASK: _task,
            ExerciseStatus.UPDATED_PROGRESS: _null,
            ExerciseStatus.CORRECT: _null,
            ExerciseStatus.WRONG: _null,
        },
    )
