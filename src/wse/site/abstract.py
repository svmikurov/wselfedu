"""Abstract base class for request handler."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

RequestParametersT = TypeVar('RequestParametersT')
ResultT = TypeVar('ResultT')


class AbstractRequestHandler(
    ABC,
    Generic[RequestParametersT, ResultT],
):
    """ABC for request handler."""

    @abstractmethod
    def handle(self, params: RequestParametersT) -> ResultT:
        """Handle the request."""
