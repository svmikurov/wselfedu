"""Domain value objects."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .protocols import Selectable, UniqueLearnable


@dataclass(frozen=True, slots=True)
class Option:
    """Option value object for a selection."""

    option_value: int
    option_text: str

    def __str__(self) -> str:
        return self.option_text

    def to_tuple(self) -> tuple[int, str]:
        """Get tuple representation."""
        return (self.option_value, self.option_text)


@dataclass(frozen=True, slots=True)
class Testing:
    """Value object for a testing exercise task."""

    question_text: str
    question_value: int
    options: list[Selectable]


@dataclass(frozen=True, slots=True)
class TaskCreating:
    """Value object for task creating."""

    learnables: list[UniqueLearnable]


@dataclass(frozen=True, slots=True)
class AnswerChecking:
    """Value object for a answer checking."""

    question_value: int
    answer_value: int


@dataclass(frozen=True, slots=True)
class CheckingResult:
    """Value object for a answer check result."""

    is_correct: bool
