"""Domain value objects."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .exceptions import (
    EmptyLearnablesError,
    InvalidOptionCountError,
    NotEnoughLearnablesError,
)

if TYPE_CHECKING:
    from .protocols import HasOptionCount, Selectable, UniqueLearnable


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

    __test__ = False

    question_text: str
    question_value: int
    options: tuple[Selectable, ...]


@dataclass(frozen=True, slots=True)
class TaskCreating:
    """Value object for task creating."""

    learnables: tuple[UniqueLearnable, ...]
    params: HasOptionCount

    def __post_init__(self) -> None:
        """Validate on creation."""
        self._validate()

    @property
    def option_count(self) -> int:
        """Testing task option count."""
        return self.params.option_count

    def _validate(self) -> None:
        """Validate all business rules."""
        self._validate_not_empty()
        self._validate_option_count()

    def _validate_not_empty(self) -> None:
        """Ensure learnables is not empty."""
        if not self.learnables:
            raise EmptyLearnablesError('Learnables cannot be empty')

    def _validate_option_count(self) -> None:
        """Ensure option count is valid."""
        if self.option_count < 1:
            raise InvalidOptionCountError(
                f'Cannot create testing task: '
                f'option count = {self.option_count} < 1'
            )

        available = len(self.learnables)

        if available < self.option_count:
            raise NotEnoughLearnablesError(
                f'Cannot create testing task: need {self.option_count} '
                f'learnables, but only {available} available'
            )


@dataclass(frozen=True, slots=True)
class AnswerChecking:
    """Value object for a answer checking."""

    question_value: int
    answer_value: int


@dataclass(frozen=True, slots=True)
class CheckingResult:
    """Value object for a answer check result."""

    is_correct: bool


###################################################
# Task configuration
###################################################


@dataclass(frozen=True, slots=True)
class TestingParameters:
    """Value object fot testing task parameters."""

    option_count: int
