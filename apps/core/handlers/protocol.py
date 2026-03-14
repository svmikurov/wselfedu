"""Protocols for request handler interface."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, TypeVar

if TYPE_CHECKING:
    from apps.users.models import Person

T_contra = TypeVar('T_contra', contravariant=True)
T_co = TypeVar('T_co', covariant=True)
Params_contra = TypeVar('Params_contra', contravariant=True)
Context_contra = TypeVar('Context_contra', contravariant=True)
Data_contra = TypeVar('Data_contra', contravariant=True)
Parsed_co = TypeVar('Parsed_co', covariant=True)
Validated_contra = TypeVar('Validated_contra', contravariant=True)
DomainResult_contra = TypeVar('DomainResult_contra', contravariant=True)
Result_co = TypeVar('Result_co', covariant=True)


class NullDataProtocol(Protocol):
    """Protocol for null data interface."""


# =================================================
# Data-Transfer-Objects
# =================================================

# -------------------------------------------------
# Request parameters
# -------------------------------------------------


class SimpleRequestParamsProtocol(Protocol):
    """Protocol for simple request parameters DTO."""


class DetailRequestParamsProtocol(Protocol):
    """Protocol for detail request parameters DTO."""

    pk: int


class QueryRequestParamsProtocol(Protocol):
    """Protocol for request with query parameters DTO."""

    query: dict[str, str]


# -------------------------------------------------
# Request context
# -------------------------------------------------


class RequestContextProtocol(Protocol):
    """Protocol for request context DTO."""

    user: Person


# -------------------------------------------------
# Request data
# -------------------------------------------------


class RequestDataProtocol(Protocol):
    """Protocol for request data DTO."""

    query: dict[str, Any]


# -------------------------------------------------
# Response data
# -------------------------------------------------


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
# Parser
# -----------------------------------------------


class RequestParserProtocol(Protocol[Parsed_co]):
    """Protocol for request parameters parse."""

    def parse(self, request_params: QueryRequestParamsProtocol) -> Parsed_co:
        """Parse request parameters."""


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
        params: DetailRequestParamsProtocol,
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


class RequestHandlerProtocol(
    Protocol[Params_contra, Context_contra, Data_contra, Result_co]
):
    """Protocol for request handler."""

    def execute(
        self,
        params: Params_contra,
        context: Context_contra,
        data: Data_contra,
    ) -> Result_co:
        """Execute."""


class RegularRequestHandlerProtocol(Protocol[T_contra, T_co]):
    """Protocol for regular request handler."""

    def execute(self, user: Person, request_data: T_contra) -> T_co:
        """Handle the request."""


class DetailRequestHandlerProtocol(Protocol[T_co]):
    """Protocol for regular request handler."""

    def execute(
        self,
        params: DetailRequestParamsProtocol,
        context: RequestContextProtocol,
        data: RequestDataProtocol,
    ) -> T_co:
        """Handle the request."""
