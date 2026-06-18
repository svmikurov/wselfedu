"""Testing exercise use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeAlias

from wse.domain import values
from wse.domain.protocols import Testable

from . import dto
from .abstract import AbstractCreateTaskUseCase
from .protocols import CerateTestingCommandProto, TaskProto

if TYPE_CHECKING:
    from wse.domain.protocols import (
        ExerciseCreatable,
        HasLearnables,
        Repository,
        UniqueLearnable,
    )

    ServiceT: TypeAlias = ExerciseCreatable[
        HasLearnables[list[UniqueLearnable]],
        Testable,
    ]


class CreateTestingUseCase(
    AbstractCreateTaskUseCase[CerateTestingCommandProto, TaskProto[Testable]]
):
    """Use case for testing task creation."""

    def __init__(
        self,
        repo: Repository,
        service: ServiceT,
    ) -> None:
        self._repo = repo
        self._service = service

    def execute(self, cmd: CerateTestingCommandProto) -> TaskProto[Testable]:
        """Create the testing task."""
        learnables = self._repo.list()
        spec = values.TaskCreating(learnables)
        task = self._service.create(spec)
        return dto.Task(task)
