"""Request data validator DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dict, Factory

from apps.core.validators.request.exercise.create_task import (
    ExerciseRequestValidator,
)
from contracts.enums.exercise import ExerciseAction
from interfaces.schemas.validator import (
    ValidatedCreateTaskRequest,
    ValidatedExerciseProgress,
)


class ValidatorContainer(DeclarativeContainer):
    """Request data validator DI container."""

    exercise_validate_schema_registry = Dict(
        {
            ExerciseAction.CREATE_TASK: ValidatedCreateTaskRequest,
            ExerciseAction.UPDATE_PROGRESS: ValidatedExerciseProgress,
        }
    )

    exercise_request = Factory(
        ExerciseRequestValidator,
        schema_class_registry=exercise_validate_schema_registry,
    )
