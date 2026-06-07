"""Application layer DTOs."""

from dataclasses import dataclass

from wse.domain.protocols import Testable


@dataclass(frozen=True, slots=True)
class ExerciseResult:
    """Exercise result DTO."""

    task: Testable
