"""Protocol for use case interface."""

from typing import Protocol, TypeVar

from utils.audit.protocol import Auditable

Command_contra = TypeVar('Command_contra', contravariant=True)
Result_co = TypeVar('Result_co', covariant=True)


class UseCaseProtocol(
    Auditable,
    Protocol[Command_contra, Result_co],
):
    """Protocol for use case."""

    def execute(
        self,
        command: Command_contra,
    ) -> Result_co:
        """Execute use case."""
