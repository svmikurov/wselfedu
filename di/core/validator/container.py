"""Request data validator DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dict, Factory

from interfaces.schemas.validator import (
    ValidatedCheckTestAnswer,
    ValidatedCreateTask,
    ValidatedExerciseProgress,
)
from kernel.validator.request.exercise.create_task import (
    ExerciseRequestValidator,
)
from ports.contract.enums.exercise import ExerciseAction


class ValidatorContainer(DeclarativeContainer):
    """Request data validator DI container."""

    exercise_validate_schema_registry = Dict(
        {
            ExerciseAction.CREATE_TASK: ValidatedCreateTask,
            ExerciseAction.CHECK_ANSWER: ValidatedCheckTestAnswer,
            ExerciseAction.UPDATE_PROGRESS: ValidatedExerciseProgress,
        }
    )

    exercise_request = Factory(
        ExerciseRequestValidator,
        schema_class_registry=exercise_validate_schema_registry,
    )
