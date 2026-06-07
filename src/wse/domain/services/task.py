"""Service for exercise task."""

from __future__ import annotations

from random import choice
from typing import TYPE_CHECKING, override

from .abstract import AbstractCreateTaskService

if TYPE_CHECKING:
    from wse.domain.protocols import Learnable


class CreateTaskService(AbstractCreateTaskService):
    """Create task service."""

    @override
    def execute(self, candidates: list[Learnable]) -> Learnable:
        """Create the exercise task."""
        return choice(candidates)
