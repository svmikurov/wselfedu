"""Protocol for exercise task interface."""

from typing import Protocol

from interfaces import enums
from interfaces.protocols.domain import exercise, general


class PresentationTaskProtocol(
    exercise.HasQuestionText,
    exercise.HasAnswerText,
    exercise.HasProgressValue,
    general.HasStatus[enums.ExerciseStatus],
    general.DumpModelProtocol[dict[str, str]],
    Protocol,
):
    """Protocol for presentation exercise task interface."""
