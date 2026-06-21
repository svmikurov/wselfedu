"""Testing exercise use case."""

from __future__ import annotations

from typing import TYPE_CHECKING

from wse.domain import values
from wse.domain.protocols import Testable

from . import dto
from .abstract import AbstractUseCase
from .protocols import (
    CerateTestingCommandProto,
    CheckResultDtoProto,
    CheckTestingCommandProto,
    TaskDtoProto,
)

if TYPE_CHECKING:
    from wse.domain.protocols import (
        AnswerCheckable,
        CheckableOption,
        ExerciseCreatable,
        HasLearnables,
        Repository,
        UniqueLearnable,
    )


class CreateTestingUseCase(
    AbstractUseCase[CerateTestingCommandProto, TaskDtoProto[Testable]]
):
    """Use case for testing task creation."""

    def __init__(
        self,
        repo: Repository[int, UniqueLearnable],
        service: ExerciseCreatable[
            HasLearnables[list[UniqueLearnable]],
            Testable,
        ],
    ) -> None:
        self._repo = repo
        self._service = service

    def execute(
        self, cmd: CerateTestingCommandProto
    ) -> TaskDtoProto[Testable]:
        """Create the testing task."""
        learnables = self._repo.list()
        # TODO: Inject a specification builder
        spec = values.TaskCreating(learnables)
        task = self._service.create(spec)
        # TODO: Inject a DTO mapper
        return dto.Task(task=task, session_id=cmd.session_id)


class CheckTestingUseCase(
    AbstractUseCase[CheckTestingCommandProto, CheckResultDtoProto]
):
    """Use case for testing answer check."""

    def __init__(
        self,
        repo: Repository[str, TaskDtoProto[Testable]],
        service: AnswerCheckable[CheckableOption, CheckResultDtoProto],
    ) -> None:
        self._repo = repo
        self._service = service

    def execute(self, cmd: CheckTestingCommandProto) -> CheckResultDtoProto:
        """Create the testing task."""
        task = self._repo.get(cmd.session_id)
        spec = values.AnswerChecking(
            question_value=task.task.question_value,
            answer_value=cmd.answer_value,
        )
        result = self._service.check(spec)
        # FIXME: Fix type ignore
        return result  # type: ignore[no-any-return]
