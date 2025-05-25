"""Defines exercise service."""

from dependency_injector import providers
from wse_exercises.base.exercise import Exercise

from services.exceptions import (
    ExerciseNotFound,
    ExerciseServiceException,
    InvalidExerciseProvider,
    TaskGenerationError,
)


class ExerciseService:
    """Service layer for exercise operations."""

    @classmethod
    def create_task(
        cls,
        container: providers.DependenciesContainer,
        exercise_type: str,
    ) -> str:
        """Create exercise task."""
        provider = cls._get_exercise_provider(container, exercise_type)
        exercise = cls._create_exercise(provider)
        return cls._generate_task(exercise)

    @classmethod
    def _get_exercise_provider(
        cls,
        container: providers.DependenciesContainer,
        exercise_type: str,
    ) -> providers.Provider:
        """Get exercise provider from container."""
        if not hasattr(container, exercise_type):
            raise ExerciseNotFound(
                f'Exercise type "{exercise_type}" not found'
            )

        provider = getattr(container, exercise_type)

        if not isinstance(provider, providers.Provider):
            raise InvalidExerciseProvider(
                f'"{exercise_type}" is not a valid exercise provider'
            )

        return provider

    @classmethod
    def _create_exercise(cls, provider: providers.Provider) -> Exercise:
        """Instantiate exercise from provider."""
        try:
            return provider()
        except Exception as e:
            raise ExerciseServiceException(
                f'Exercise initialization failed: {str(e)}'
            ) from e

    @classmethod
    def _generate_task(cls, exercise: Exercise) -> str:
        """Generate task JSON from exercise."""
        try:
            task = exercise.create_task()
            return task.model_dump_json()
        except Exception as e:
            raise TaskGenerationError(
                f'Task generation failed: {str(e)}'
            ) from e
