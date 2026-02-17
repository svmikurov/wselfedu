"""Abstract base class for request validator."""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from apps.core.handlers.protocol import RequestDataProtocol

Validated = TypeVar('Validated')


class AbstractRegularValidator(ABC, Generic[Validated]):
    """ABC for regular request validator."""

    @classmethod
    @abstractmethod
    def validate(cls, raw_data: dict[str, Any]) -> Validated:
        """Validate request data."""


class AbstractDetailValidator(ABC, Generic[Validated]):
    """ABC for detail request validator."""

    @classmethod
    @abstractmethod
    def validate(cls, data: RequestDataProtocol) -> Validated:
        """Validate request data."""
