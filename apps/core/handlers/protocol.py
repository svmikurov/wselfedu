"""Protocols for request handler interface."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, TypeVar

if TYPE_CHECKING:
    from apps.users.models import Person

T_contra = TypeVar('T_contra', contravariant=True)
T_co = TypeVar('T_co', covariant=True)


# ===============================================
# Data-Transfer-Objects
# ===============================================


class RequestContextProtocol(Protocol):
    """Protocol for request context DTO."""

    user: Person


class DetailParamsProtocol(Protocol):
    """Protocol for detail request parameters DTO."""

    pk: int


class RequestDataProtocol(Protocol):
    """Protocol for request data DTO."""

    query: dict[str, Any]


class RequestResultProtocol(Protocol):
    """Protocol for request handling result DTO."""

    context: dict[str, Any]


# ===============================================
# Dependencies
# ===============================================


# -----------------------------------------------
# Validator
# -----------------------------------------------


class RegularValidator(Protocol[T_contra, T_co]):
    """Protocol for regular validator interface."""

    @classmethod
    def validate(cls, raw_data: T_contra) -> T_co:
        """Validate raw data."""


class DetailValidator(Protocol[T_co]):
    """Protocol for validator with identifier."""

    @classmethod
    def validate(cls, data: RequestDataProtocol) -> T_co:
        """Validate raw data with identifier."""


# Deprecated
class ResourceValidator(Protocol[T_contra, T_co]):
    """Protocol for validator with identifier."""

    @classmethod
    def validate(cls, raw_data: T_contra, pk: int) -> T_co:
        """Validate raw data with identifier."""


# -----------------------------------------------
# UseCase
# -----------------------------------------------


class SimpleUseCase(Protocol[T_co]):
    """Protocol for UseCase interface without input data."""

    def execute(self, user: Person) -> T_co:
        """Execute business logic."""


class UseCase(Protocol[T_contra, T_co]):
    """Protocol for UseCase interface with input data."""

    def execute(self, user: Person, request_data: T_contra) -> T_co:
        """Execute business logic."""


class DetailUseCase(Protocol[T_contra, T_co]):
    """Protocol for UseCase interface with input data."""

    def execute(
        self,
        params: DetailParamsProtocol,
        context: RequestContextProtocol,
        validated: T_contra,
    ) -> T_co:
        """Execute business logic."""


# -----------------------------------------------
# Adapter
# -----------------------------------------------


# DEPRECATED: Delete response adapter
class ResponseAdapterDeprecated(Protocol[T_contra, T_co]):
    """Protocol for response adapter interface."""

    def to_response(self, domain_result: T_contra) -> T_co:
        """Convert to response."""


class ResponseAdapter(Protocol[T_contra]):
    """Protocol for response adapter interface."""

    def to_response(self, domain_result: T_contra) -> RequestResultProtocol:
        """Convert to response."""


# -----------------------------------------------
# Handler
# -----------------------------------------------


class RequestHandlerProtocol(Protocol[T_contra, T_co]):
    """Protocol for request parameters handler."""

    def execute(self, request_data: T_contra) -> T_co:
        """Handle the request."""


class RegularRequestHandlerProtocol(Protocol[T_contra, T_co]):
    """Protocol for regular request handler."""

    def execute(self, user: Person, request_data: T_contra) -> T_co:
        """Handle the request."""


class DetailRequestHandlerProtocol(Protocol[T_co]):
    """Protocol for regular request handler."""

    def execute(
        self,
        params: DetailParamsProtocol,
        context: RequestContextProtocol,
        data: RequestDataProtocol,
    ) -> T_co:
        """Handle the request."""
