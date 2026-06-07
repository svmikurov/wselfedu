"""Application use cases."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from .abstract import AbstractCreateTaskUseCase

if TYPE_CHECKING:
    from wse.domain.protocols import (
        CandidatesRepositoryProtocol,
        CreateTaskServiceProtocol,
        Learnable,
    )


class CreateTaskUseCase(AbstractCreateTaskUseCase):
    """Create task use case."""

    def __init__(
        self,
        repository: CandidatesRepositoryProtocol,
        domain: CreateTaskServiceProtocol,
    ) -> None:
        self._repository = repository
        self._domain = domain

    @override
    def execute(self) -> Learnable:
        """Create the task."""
        candidates = self._repository.list()
        task = self._domain.execute(candidates)
        return task
