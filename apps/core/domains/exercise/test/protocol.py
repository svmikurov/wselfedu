"""Protocol for test exercise interface."""

from typing import Protocol

from interfaces.entity.domain.exercise import fields


class TestExerciseCaseProtocol(
    fields.HasQuestionOptionValue,
    fields.HasExerciseDomainOptions,
    Protocol,
):
    """Protocol for test exercise case DTO interface."""


class TestExerciseDomainResultProtocol(
    fields.HasExerciseStatus,
    fields.HasCase[TestExerciseCaseProtocol],
    Protocol,
):
    """Protocol for test exercise domain result DTO interface."""


class TestExerciseTaskProtocol(
    fields.HasExerciseStatus,
    fields.HasQuestionText,
    fields.HasExerciseDomainOptions,
    Protocol,
):
    """Protocol for test exercise task DTO interface."""
