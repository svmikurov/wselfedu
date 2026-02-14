"""Abstract base class for request validator."""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

Validated = TypeVar('Validated')


class AbstractRegularValidator(ABC, Generic[Validated]):
    """ABC for regular request validator."""

    @classmethod
    @abstractmethod
    def validate(cls, raw_data: dict[str, Any]) -> Validated:
        """Validate request data."""
