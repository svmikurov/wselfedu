"""Exercise perform request data interfaces."""

from typing import Protocol

from contracts.entity.domain.exercise.fields import HasOptionValue
from contracts.entity.domain.general import HasAction
from contracts.enums import ExerciseAction


class ValidatedCreateTaskRequestProtocol(
    HasAction[ExerciseAction],
    Protocol,
):
    """Protocol for *create task* request data interface."""


class ValidatedCheckTestRequestProtocol(
    HasAction[ExerciseAction],
    HasOptionValue,
    Protocol,
):
    """Protocol for *check test answer* request data interface."""
