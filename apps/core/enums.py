"""Defines base class for enumerations."""

from enum import Enum


class BaseEnum(str, Enum):
    """Base class for enumerations."""

    def __str__(self) -> str:
        """Return button text."""
        return str(self.value)
