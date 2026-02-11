"""Abstract base class for request validator."""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T_co = TypeVar('T_co', covariant=True)


class AbstractRegularValidator(Generic[T_co], ABC):
    """ABC for regular request validator."""

    @classmethod
    @abstractmethod
    def validate(cls, raw_data: dict[str, Any]) -> T_co:
        """Validate request data."""
