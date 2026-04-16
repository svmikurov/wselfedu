"""Protocols for core exercise service."""

from typing import Protocol, TypeVar

from apps.users.models import Person

Result_cov = TypeVar('Result_cov', covariant=True)
Parameters_contra = TypeVar('Parameters_contra', contravariant=True)

Filter = TypeVar('Filter')
Updates = TypeVar('Updates')
Filter_cov = TypeVar('Filter_cov', covariant=True)
Updates_cov = TypeVar('Updates_cov', covariant=True)


class HasRepositoryUserCommand(Protocol[Filter, Updates]):
    """Protocol for service command interface."""

    user: Person
    filter: Filter
    updates: Updates


class CreateExerciseProtocol(Protocol[Parameters_contra, Result_cov]):
    """ABC for service to create the exercise case."""

    def execute(
        self,
        user: Person,
        spec: Parameters_contra,
    ) -> Result_cov:
        """Create the exercise case."""
