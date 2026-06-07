"""Abstract base classes for infrastructure."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wse.domain.protocols import UniqueLearnable


class AbstractRepository(ABC):
    """ABC for task candidates repository."""

    @abstractmethod
    def list(self) -> list[UniqueLearnable]:
        """Get candidates."""
