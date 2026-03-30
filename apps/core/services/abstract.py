"""ABC for service."""

from abc import ABC, abstractmethod
from typing import TypeVar, override

from apps.users.models import Person

from .protocol import ServiceProtocol

Data = TypeVar('Data')
Result = TypeVar('Result')


class AbstractUserService(
    ABC,
    ServiceProtocol[Data, Result],
):
    """ABC for user's service."""

    @override
    @abstractmethod
    def execute(self, user: Person, data: Data) -> Result:
        """Execute."""
