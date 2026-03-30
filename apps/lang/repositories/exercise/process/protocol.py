"""Protocol for process exercise repository."""

from typing import Protocol, TypeVar

from apps.users.models import Person

Command_contra = TypeVar('Command_contra', contravariant=True)
Result_cov = TypeVar('Result_cov', covariant=True)


class ProcessExerciseRepositoryProtocol(Protocol[Command_contra, Result_cov]):
    """Protocol for process exercise repository."""

    def update(self, user: Person, command: Command_contra) -> Result_cov:
        """Update."""
