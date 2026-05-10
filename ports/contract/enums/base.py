"""Base class for enumerations."""

from enum import Enum


class BaseEnum(str, Enum):
    """Base class for enumerations."""

    def __str__(self) -> str:
        """Return string representation of enumeration."""
        return str(self.value)
