"""Protocols for exercise interface."""

from __future__ import annotations

from typing import Iterator, Protocol, Self, overload
from uuid import UUID

from apps.core.domains.exercise import ExerciseStatusEnum

from . import DisplayOrder

# ------------------------------------
# Exercise configuration DTO interface
# ------------------------------------


class ExerciseStatus(Protocol):
    """Protocol for exercise case status."""

    exercise_status: ExerciseStatusEnum


class Conditions(Protocol):
    """Regular exercise items lookup conditions interface."""


class Settings(Protocol):
    """Regular exercise settings interface."""

    display_order: DisplayOrder
    option_count: int
    item_count: int


class Parameters(Protocol):
    """Regular exercise parameters interface."""

    conditions: Conditions
    settings: Settings


class ExerciseConfig(Protocol):
    """Test exercise configuration interface interface."""

    display_order: DisplayOrder
    option_count: int
    item_count: int


# -----------------------------------
# Exercise case request DTO interface
# -----------------------------------


class ExerciseRequest(ExerciseStatus):
    """Interface for exercise case request."""

    case_uuid: UUID
    pk: int


# ----------------------
# Exercise DTO interface
# ----------------------


class Candidate(Protocol):
    """Protocol for a single candidate item."""

    pk: int
    define: str
    explain: str
    progress: int


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


class ExerciseCase(Protocol):
    """Exercise case interface."""


class ExerciseCaseMeta(Protocol):
    """Exercise case meta interface."""


class StoredCase(Protocol):
    """Stored exercise case interface."""


# ----------------------------
# Exercise check DTO interface
# ----------------------------


class TestCheckRequest(ExerciseStatus):
    """Interface for user's answer on test exercise check request."""

    case_uuid: UUID
    option_value: int


class CheckResultProtocol(Protocol):
    """User answer check result."""

    is_correct: bool


class Explanation(Protocol):
    """Exercise explanation interface."""
