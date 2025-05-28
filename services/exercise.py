"""Defines exercise service."""

import logging

from dependency_injector import providers
from wse_exercises.core.mathem.base.exercise import (
    BaseSimpleCalculationExercise,
    SimpleMathExerciseConfig,
    SimpleMathTaskRequest,
)
from wse_exercises.core.mathem.enums import Exercises
from wse_exercises.core.mathem.task import SimpleMathTask

from services.base import BaseSimpleMathExerciseService
from services.exceptions import (
    ExerciseNotFound,
    ExerciseServiceException,
    TaskGenerationError,
)

logger = logging.getLogger(__name__)


class SimpleMathExerciseService(BaseSimpleMathExerciseService):
    """Service layer for exercise operations."""

    def __init__(
        self,
        exercises_container: providers.DependenciesContainer,
    ) -> None:
        """Construct the service."""
        self.exercises_container = exercises_container

    def create_task(
        self,
        task_request_dto: SimpleMathTaskRequest,
    ) -> SimpleMathTask:
        """Create simple matn calculation task."""
        provider = self._get_exercise_provider(task_request_dto.name)
        exercise = self._create_exercise(provider)
        task = self._generate_task(task_request_dto.config, exercise)
        return task

    @staticmethod
    def _create_exercise(
        provider: providers.Provider,
    ) -> BaseSimpleCalculationExercise:
        try:
            exercise = provider()
        except Exception as e:
            logger.exception('Exercise initialisation failed')
            raise ExerciseServiceException(
                f'Exercise initialisation failed:  {str(e)}'
            ) from e

        return exercise

    def _get_exercise_provider(
        self,
        exercise_name: Exercises,
    ) -> providers.Provider:
        try:
            return getattr(self.exercises_container, exercise_name)
        except AttributeError as e:
            logger.exception(f'Exercise name "{exercise_name}" not found')
            raise ExerciseNotFound(
                f'Exercise name "{exercise_name}" not found'
            ) from e

    @staticmethod
    def _generate_task(
        config: SimpleMathExerciseConfig,
        exercise: BaseSimpleCalculationExercise,
    ) -> SimpleMathTask:
        try:
            return exercise.create_task(config)
        except Exception as err:
            logger.exception('Task generation failed')
            raise TaskGenerationError(
                f'Task generation failed: {str(err)}'
            ) from err
