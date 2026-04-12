"""Protocol for exercise use case."""

from typing import Protocol, TypeVar

Command_contra = TypeVar('Command_contra', contravariant=True)
Result_cov = TypeVar('Result_cov', covariant=True)

# =================================================
# UseCase some dependencies interface
# =================================================


class ResolverProtocol(Protocol[Command_contra, Result_cov]):
    """Protocol for resolver."""

    def resolve(
        self,
        command: Command_contra,
    ) -> Result_cov:
        """Resolve."""


# =================================================
# UseCase interface
# =================================================


class UseCaseProtocol(Protocol[Command_contra, Result_cov]):
    """Protocol for use case."""

    def execute(
        self,
        command: Command_contra,
    ) -> Result_cov:
        """Execute use case."""
