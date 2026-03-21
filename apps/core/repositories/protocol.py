"""Protocol for repository."""

from typing import Protocol, TypeVar

FilterData_contra = TypeVar('FilterData_contra', contravariant=True)
Query_cov = TypeVar('Query_cov', covariant=True)
Result_cov = TypeVar('Result_cov', covariant=True)


class RepositoryProtocol(Protocol[FilterData_contra, Result_cov]):
    """Protocol for repository that returns DTO."""

    def fetch(self, filter: FilterData_contra) -> Result_cov:
        """Fetch data."""


class ModelRepositoryProtocol(Protocol[FilterData_contra, Query_cov]):
    """Protocol for repository that returns ORM model query."""

    def get_query(self, filter: FilterData_contra) -> Query_cov:
        """Fetch model."""
