"""Abstract base class http entrypoint layer."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

RequestParamsT = TypeVar('RequestParamsT')
RequestContextT = TypeVar('RequestContextT')
RequestDataT = TypeVar('RequestDataT')
ResultT = TypeVar('ResultT')


class AbstractRequestHandler(
    ABC,
    Generic[RequestParamsT, RequestContextT, RequestDataT, ResultT],
):
    """ABC for request handler."""

    @abstractmethod
    def handle(
        self,
        params: RequestParamsT,
        context: RequestContextT,
        data: RequestDataT,
    ) -> ResultT:
        """Handle the request."""
