"""Protocol for resolver interface."""

from typing import Protocol, TypeVar

Command_contra = TypeVar('Command_contra', contravariant=True)
Result_co = TypeVar('Result_co', covariant=True)


class ResolverProtocol(Protocol[Command_contra, Result_co]):
    """Protocol for resolver."""

    def resolve(
        self,
        command: Command_contra,
    ) -> Result_co:
        """Resolve."""
