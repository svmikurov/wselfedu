"""Protocols for request handler interface."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, TypeVar

if TYPE_CHECKING:
    from apps.users.models import Person

T_contra = TypeVar('T_contra', contravariant=True)
T_co = TypeVar('T_co', covariant=True)

# -----------------------------------------------
# Validator
# -----------------------------------------------


class RegularValidator(Protocol[T_contra, T_co]):
    """Protocol for regular validator interface."""

    @classmethod
    def validate(cls, raw_data: T_contra) -> T_co:
        """Validate raw data."""


class DetailValidator(Protocol[T_contra, T_co]):
    """Protocol for validator with identifier."""

    @classmethod
    def validate(cls, raw_data: T_contra, pk: int) -> T_co:
        """Validate raw data with identifier."""


# -----------------------------------------------
# Service
# -----------------------------------------------


class SimpleService(Protocol[T_co]):
    """Protocol for simple business service interface."""

    def execute(self, user: Person) -> T_co:
        """Execute business logic."""


class BusinessService(Protocol[T_contra, T_co]):
    """Protocol for business service interface."""

    def execute(
        self, user: Person, query_parameters: T_contra | None = None
    ) -> T_co:
        """Execute business logic."""


# -----------------------------------------------
# Adapter
# -----------------------------------------------


class ResponseAdapter(Protocol[T_contra, T_co]):
    """Protocol for response adapter interface."""

    def to_response(self, domain_result: T_contra) -> T_co:
        """Convert to response."""


# -----------------------------------------------
# Handler
# -----------------------------------------------


class RegularRequestHandlerProtocol(Protocol[T_contra, T_co]):
    """Protocol for regular request handler."""

    def execute(self, user: Person, request_data: T_contra) -> T_co:
        """Handle the request."""
