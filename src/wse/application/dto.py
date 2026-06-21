"""Data transfer objects."""

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar('T')


@dataclass(frozen=True, slots=True)
class Task(Generic[T]):
    """Testing task DTO."""

    task: T
    session_id: str
