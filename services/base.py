"""Definers abstract base class for exercise services."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from wse_exercises.base.exercise import TaskRequest
from wse_exercises.base.interface import ITask
from wse_exercises.core.mathem.base.exercise import SimpleMathTaskRequest
from wse_exercises.core.mathem.task import SimpleMathTask

_TaskRequest = TypeVar('_TaskRequest', bound=TaskRequest)
_Task = TypeVar('_Task', bound=ITask)


class BaseExerciseService(ABC, Generic[_TaskRequest, _Task]):
    """Base absract class for exercise services."""

    @abstractmethod
    def create_task(
        self,
        exercise_request: _TaskRequest,
    ) -> _Task:
        """Create simple matn calculation task."""


class BaseSimpleMathExerciseService(
    BaseExerciseService[SimpleMathTaskRequest, SimpleMathTask],
    ABC,
):
    """Abstract base class for simple math task creation."""

    @abstractmethod
    def create_task(
        self,
        task_request_dto: SimpleMathTaskRequest,
    ) -> SimpleMathTask:
        """Create simple matn calculation task."""
