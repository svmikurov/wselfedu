"""Abstract base classes for request handlers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from apps.users.models import Person

T_co = TypeVar('T_co', covariant=True)
T_contra = TypeVar('T_contra', contravariant=True)


class AbstractSimpleHandler(ABC, Generic[T_co]):
    """ABC for simple request handler."""

    @abstractmethod
    def execute(self, user: Person) -> T_co:
        """Execute use case."""


class AbstractHandler(ABC, Generic[T_contra, T_co]):
    """ABC for request handler."""

    @abstractmethod
    def execute(self, user: Person, request_data: T_contra) -> T_co:
        """Execute use case."""
