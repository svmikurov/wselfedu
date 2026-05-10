"""Protocol for repository."""

from typing import Protocol, TypeVar

from apps.users.models import Person
from utils.audit.protocol import Auditable

FilterData_contra = TypeVar('FilterData_contra', contravariant=True)
UpdateData_contra = TypeVar('UpdateData_contra', contravariant=True)
Command_contra = TypeVar('Command_contra', contravariant=True)

Query_co = TypeVar('Query_co', covariant=True)
Result_co = TypeVar('Result_co', covariant=True)


class RepositoryProtocol(Protocol[FilterData_contra, Result_co]):
    """Protocol for user's resource repository provides DTO."""

    def fetch(
        self,
        user: Person,
        filter: FilterData_contra,
    ) -> Result_co:
        """Fetch data."""


class CommandRepositoryProtocol(
    Auditable,
    Protocol[Command_contra, Result_co],
):
    """Protocol for user command repository."""

    def update(self, user: Person, command: Command_contra) -> Result_co:
        """Update."""
