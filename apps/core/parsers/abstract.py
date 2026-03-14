"""Abstract base classes for request parameters parse."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Parsed = TypeVar('Parsed')
RequestParams = TypeVar('RequestParams')


class AbstractRequestParser(ABC, Generic[RequestParams, Parsed]):
    """ABC for request parameters parse."""

    @abstractmethod
    def parse(self, params: RequestParams) -> Parsed:
        """Parse request parameters."""
