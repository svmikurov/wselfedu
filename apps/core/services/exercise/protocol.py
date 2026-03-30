"""Protocols for core exercise service."""

from typing import Protocol, TypeVar

from apps.users.models import Person

Result_cov = TypeVar('Result_cov', covariant=True)
Parameters_contra = TypeVar('Parameters_contra', contravariant=True)


class CreateExerciseProtocol(Protocol[Parameters_contra, Result_cov]):
    """ABC for service to create the exercise case."""

    def execute(
        self,
        parameters: Parameters_contra,
        user: Person,
    ) -> Result_cov:
        """Create the exercise case."""
