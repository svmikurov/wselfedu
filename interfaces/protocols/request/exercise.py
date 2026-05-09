"""Exercise perform request data interfaces."""

from typing import Protocol

from contracts.entity.domain.exercise.fields import HasOptionValue
from contracts.entity.domain.general import HasAction
from contracts.enums import ExerciseAction


class CheckTestRequestDataProtocol(
    HasAction[ExerciseAction],
    HasOptionValue,
    Protocol,
):
    """Protocol for check test request data interface."""
