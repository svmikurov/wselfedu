"""Abstract base class for service."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, TypeVar, override

from .protocol import UserServiceProtocol

if TYPE_CHECKING:
    from apps.users.models import Person

SpecT = TypeVar('SpecT')
ResultT = TypeVar('ResultT')


class AbstractUserService(
    ABC,
    UserServiceProtocol[SpecT, ResultT],
):
    """ABC for user's service."""

    @override
    @abstractmethod
    def execute(self, user: Person, spec: SpecT) -> ResultT:
        """Execute."""
