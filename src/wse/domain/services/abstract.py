"""Abstract base classes for domain service."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, override

from wse.domain.protocols import CreateTaskServiceProtocol

if TYPE_CHECKING:
    from wse.domain.protocols import Learnable


class AbstractCreateTaskService(ABC, CreateTaskServiceProtocol):
    """ABC for create task service."""

    @override
    @abstractmethod
    def execute(self, candidates: list[Learnable]) -> Learnable:
        """Create the task."""
