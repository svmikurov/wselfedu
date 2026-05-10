"""Web request interface."""

from typing import Protocol, TypeVar

QueryData = TypeVar('QueryData')
RequestData = TypeVar('RequestData')


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
