"""Abstract base classes for use case."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wse.domain.protocols import Learnable


class AbstractCreateTaskUseCase(ABC):
    """ABC for create task use case."""

    @abstractmethod
    def execute(self) -> Learnable:
        """Create the task."""
