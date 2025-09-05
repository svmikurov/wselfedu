"""Types for exercise services."""

import uuid
from abc import ABC, abstractmethod
from typing import Protocol, TypedDict, TypeVar

from typing_extensions import override
from wse_exercises.core.math import CalcTask

TaskT_cov = TypeVar('TaskT_cov', covariant=True)


class CalcConfigDict(TypedDict):
    """Type for calculation task config."""

    min_value: int
    max_value: int


class CalcConditionType(TypedDict):
    """Type for calculation task conditions."""

    exercise_name: str
    config: CalcConfigDict


class CalcTaskType(TypedDict):
    """Type for calculation task."""

    uid: uuid.UUID
    question: str


class CalcAnswerType(TypedDict):
    """Type for user answer on calculation task."""

    uid: uuid.UUID
    answer: str


class AssignedCalcAnswerType(CalcAnswerType):
    """Type for user answer on assigned calculation task."""

    assignation_id: str


class ResultType(TypedDict):
    """Type for user answer check result."""

    is_correct: bool


class ExerciseServiceProt(
    Protocol[TaskT_cov],
):
    """Protocol for task creation service interface."""

    def create_task(self, data: CalcConditionType) -> TaskT_cov:
        """Create task."""


class BaseCalcService(
    ABC,
    ExerciseServiceProt[CalcTask],
):
    """Abstract base class of service for creating calculation tasks."""

    @abstractmethod
    @override
    def create_task(self, data: CalcConditionType) -> CalcTask:
        """Create calculation task."""
