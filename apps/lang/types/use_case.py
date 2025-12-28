"""UseCase types."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, TypeVar

if TYPE_CHECKING:
    from apps.users.models import Person

T_contra = TypeVar('T_contra', contravariant=True)
T_co = TypeVar('T_co', covariant=True)


class Validator(Protocol[T_contra, T_co]):
    """Protocol for validator interface."""

    @classmethod
    def validate(cls, raw_data: T_contra) -> T_co:
        """Validate raw data."""


class BusinessService(Protocol[T_contra, T_co]):
    """Protocol for business service interface."""

    def execute(self, user: Person, query_parameters: T_contra) -> T_co:
        """Execute business logic."""


class ResponseAdapter(Protocol[T_contra, T_co]):
    """Protocol for response adapter interface."""

    def to_response(self, domain_result: T_contra) -> T_co:
        """Convert to response."""
