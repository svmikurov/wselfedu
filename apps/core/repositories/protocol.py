"""Protocol for repository."""

from typing import Protocol, TypeVar

from apps.users.models import Person

FilterData_contra = TypeVar('FilterData_contra', contravariant=True)
UpdateData_contra = TypeVar('UpdateData_contra', contravariant=True)
Query_co = TypeVar('Query_co', covariant=True)
Result_co = TypeVar('Result_co', covariant=True)


class UpdateRepositoryProtocol(
    Protocol[FilterData_contra, UpdateData_contra, Result_co],
):
    """Protocol for repository interface."""

    def update(
        self,
        user: Person,
        filter: FilterData_contra,
        updates: UpdateData_contra,
    ) -> Result_co:
        """Update."""


class UserRepositoryProtocol(Protocol[FilterData_contra, Result_co]):
    """Protocol for user's resource repository provides DTO."""

    def fetch(
        self,
        user: Person,
        filter: FilterData_contra,
    ) -> Result_co:
        """Fetch data."""


class ModelRepositoryProtocol(Protocol[FilterData_contra, Query_co]):
    """Protocol for repository provides ORM model query."""

    def get_query(self, filter: FilterData_contra) -> Query_co:
        """Fetch model."""
