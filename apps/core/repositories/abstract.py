"""Abstract base class for repository."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, TypeVar, override

from .protocol import UserCommandRepositoryProtocol, UserRepositoryProtocol

if TYPE_CHECKING:
    from apps.users.models import Person

FilterT = TypeVar('FilterT')
ResultT = TypeVar('ResultT')
CommandT = TypeVar('CommandT')


class AbstractUserFetchRepository(
    ABC,
    UserRepositoryProtocol[FilterT, ResultT],
):
    """ABC for fetch repository via user filter."""

    @override
    @abstractmethod
    def fetch(self, user: Person, filter: FilterT) -> ResultT:
        """Fetch."""


# =================================================
# ABC for user's command repository
# =================================================


class AbstractProcessExerciseRepository(
    ABC,
    UserCommandRepositoryProtocol[CommandT, ResultT],
):
    """ABC for process exercise repository."""

    @override
    @abstractmethod
    def update(self, user: Person, command: CommandT) -> ResultT:
        """Update study progress.

        Parameter
        ---------
        user : `Person`
            Item owner.
        command : `CommandT`
            Command DTO to update progress.
        """
