"""Language app's request data validator DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory

from apps.core.validators.request.exercise.create_task import (
    CreateExerciseTaskValidator,
)


class LangValidatorContainer(DeclarativeContainer):
    """Language app's request data validator DI container."""

    new_task = Factory(
        CreateExerciseTaskValidator,
    )
