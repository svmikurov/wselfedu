"""Protocols for request handler interface."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, TypeVar

if TYPE_CHECKING:
    from apps.users.models import Person

HandlerT = TypeVar('HandlerT')

# Request
QueryData = TypeVar('QueryData')
Params_contra = TypeVar('Params_contra', contravariant=True)
Context_contra = TypeVar('Context_contra', contravariant=True)
Data_contra = TypeVar('Data_contra', contravariant=True)

RequestData = TypeVar('RequestData')

# Prepared request data for use case
Parsed_cov = TypeVar('Parsed_cov', covariant=True)
RequestData_contra = TypeVar('RequestData_contra', contravariant=True)
Validated = TypeVar('Validated')

# Result data
Result_cov = TypeVar('Result_cov', covariant=True)
ResultContext = TypeVar('ResultContext')


# =================================================
# Data-Transfer-Objects
# =================================================

# -------------------------------------------------
# Request
# -------------------------------------------------


class QueryRequestParamsProtocol(Protocol[QueryData]):
    """Protocol for request with query parameters DTO."""

    query: QueryData


class DetailRequestParamsProtocol(Protocol):
    """Protocol for detail request parameters DTO."""

    pk: int


class DetailQueryRequestParamsProtocol(
    QueryRequestParamsProtocol[QueryData],
    DetailRequestParamsProtocol,
    Protocol,
):
    """Protocol for request with detail query parameters DTO."""


class RequestDataProtocol(Protocol[RequestData]):
    """Protocol for request data DTO."""

    data: RequestData


class ValidatedDataProtocol(Protocol[Validated]):
    """Protocol for validated data DTO."""

    data: Validated


# -------------------------------------------------
# Response
# -------------------------------------------------


class RequestResultProtocol(Protocol[ResultContext]):
    """Protocol for request handling result DTO."""

    context: ResultContext


# ===============================================
# Handler's dependencies
# ===============================================

# -----------------------------------------------
# Parser
# -----------------------------------------------


class RequestParserProtocol(Protocol[QueryData, Parsed_cov]):
    """Protocol for request parameters parse."""

    def parse(
        self,
        request_params: QueryRequestParamsProtocol[QueryData],
    ) -> Parsed_cov:
        """Parse request parameters."""


# -----------------------------------------------
# Handler
# -----------------------------------------------


class HasHandler(Protocol[HandlerT]):
    """Protocol for has *handler* interface."""

    handler: HandlerT


class RequestHandlerProtocol(
    Protocol[Params_contra, Context_contra, Data_contra, Result_cov]
):
    """Protocol for request handler."""

    def execute(
        self,
        params: Params_contra,
        context: Context_contra,
        data: Data_contra,
    ) -> Result_cov:
        """Execute."""
