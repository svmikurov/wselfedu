"""Protocols for exercise's domain interface."""

from typing import Iterator, Protocol, Self, overload

from contracts.entity.domain.exercise.fields import (
    HasAnswerText,
    HasDefineText,
    HasExerciseDomainOptions,
    HasMeanText,
    HasProgressValue,
    HasQuestionOptionValue,
    HasQuestionText,
)
from contracts.entity.domain.general import HasResourceIdentifier

# =================================================
# Exercise task
# =================================================


class Candidate(
    HasResourceIdentifier,
    HasDefineText,
    HasMeanText,
    HasProgressValue,
    Protocol,
):
    """Protocol for a single candidate item."""


class Candidates(Protocol):
    """Protocol for a collection of candidates."""

    def __iter__(self) -> Iterator[Candidate]:
        """Return an iterator over candidates in the collection."""
        ...

    def __len__(self) -> int:
        """Return the number of candidates in the collection."""
        ...

    @overload
    def __getitem__(self, index: int) -> Candidate: ...
    @overload
    def __getitem__(self, items_slice: slice) -> Self: ...
    def __getitem__(self, index_or_slice: int | slice) -> Candidate | Self:
        """Get a candidate by index or a slice of the collection."""
        ...

    def order_by(self, *field_names: str) -> Self:
        """Order the collection by one or more fields."""
        ...


class PresentationTaskProtocol(
    HasQuestionText,
    HasAnswerText,
    HasProgressValue,
    Protocol,
):
    """Protocol for presentation exercise task interface."""


class TestTaskProtocol(
    HasQuestionOptionValue,
    HasExerciseDomainOptions[Candidates],
    Protocol,
):
    """Protocol for test exercise task interface."""
