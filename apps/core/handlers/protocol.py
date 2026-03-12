"""Protocols for request handler interface."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, TypeVar

if TYPE_CHECKING:
    from apps.users.models import Person

T_contra = TypeVar('T_contra', contravariant=True)
T_co = TypeVar('T_co', covariant=True)
Params_contra = TypeVar('Params_contra', contravariant=True)
Context_contra = TypeVar('Context_contra', contravariant=True)
Validated_contra = TypeVar('Validated_contra', contravariant=True)
DomainResult_contra = TypeVar('DomainResult_contra', contravariant=True)
Result_co = TypeVar('Result_co', covariant=True)


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


class OobResultProtocol(Protocol):
    """Protocol for response result DTO with OOB content."""

    context: dict[str, Any]
    oob_html: str


# ===============================================
# Dependencies
# ===============================================


# -----------------------------------------------
# Validator
# -----------------------------------------------


class ValidatorProtocol(Protocol[T_contra, T_co]):
    """Protocol for regular validator interface."""

    @classmethod
    def validate(cls, raw_data: T_contra) -> T_co:
        """Validate raw data."""


class RequestValidatorProtocol(Protocol[T_co]):
    """Protocol for request validator interface."""

    @classmethod
    def validate(cls, data: RequestDataProtocol) -> T_co:
        """Validate data."""


# Deprecated
class ResourceValidatorProtocol(Protocol[T_contra, T_co]):
    """Protocol for validator with identifier."""

    @classmethod
    def validate(cls, raw_data: T_contra, pk: int) -> T_co:
        """Validate raw data with identifier."""


# -----------------------------------------------
# UseCase
# -----------------------------------------------


class SimpleUseCaseProtocol(Protocol[T_co]):
    """Protocol for UseCase interface without input data."""

    def execute(self, user: Person) -> T_co:
        """Execute business logic."""


class DataUseCaseProtocol(Protocol[T_contra, T_co]):
    """Protocol for UseCase interface with input data."""

    def execute(self, user: Person, request_data: T_contra) -> T_co:
        """Execute business logic."""


class DetailUseCaseProtocol(Protocol[T_contra, T_co]):
    """Protocol for UseCase interface with input data."""

    def execute(
        self,
        params: DetailParamsProtocol,
        context: RequestContextProtocol,
        validated: T_contra,
    ) -> T_co:
        """Execute business logic."""


class UseCaseProtocol(
    Protocol[Params_contra, Context_contra, Validated_contra, Result_co]
):
    """Protocol for generic UseCase interface."""

    def execute(
        self,
        params: Params_contra,
        context: Context_contra,
        validated: Validated_contra,
    ) -> Result_co:
        """Execute business logic."""


# -----------------------------------------------
# Adapter
# -----------------------------------------------


class GenericAdapterProtocol(Protocol[T_contra, T_co]):
    """Protocol for response adapter interface."""

    def to_response(self, domain_result: T_contra) -> T_co:
        """Convert to response."""


class ResponseAdapterProtocol(Protocol[T_contra]):
    """Protocol for response adapter interface.

    Does not use request context.
    """

    def to_response(self, schema: T_contra) -> RequestResultProtocol:
        """Convert to response."""


class ContextResponseAdapterProtocol(Protocol[T_contra]):
    """Protocol for response adapter interface.

    Uses request context.
    """

    def to_response(
        self,
        schema: T_contra,
        request_context: RequestContextProtocol,
    ) -> RequestResultProtocol:
        """Convert to response."""


class AdapterProtocol(
    Protocol[DomainResult_contra, Context_contra, Result_co]
):
    """Protocol for response adapter interface.

    Uses request context.
    """

    def to_response(
        self,
        schema: DomainResult_contra,
        request_context: Context_contra,
    ) -> Result_co:
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
