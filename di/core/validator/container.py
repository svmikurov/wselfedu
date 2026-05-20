"""Request data validator DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dict, Factory

from kernel.validator.request.exercise.create_task import (
    ExerciseRequestValidator,
)
from ports.contract.enums.exercise import ExerciseAction
from ports.interfaces.schemas.handler import (
    CheckTestAnswerSchema,
    CreateTaskSchema,
    ProgressUpdateSchema,
)


class ValidatorContainer(DeclarativeContainer):
    """Request data validator DI container."""

    exercise_validate_schema_registry = Dict(
        {
            ExerciseAction.CREATE_TASK: CreateTaskSchema,
            ExerciseAction.CHECK_ANSWER: CheckTestAnswerSchema,
            ExerciseAction.UPDATE_PROGRESS: ProgressUpdateSchema,
        }
    )

    exercise_request = Factory(
        ExerciseRequestValidator,
        schema_class_registry=exercise_validate_schema_registry,
    )
