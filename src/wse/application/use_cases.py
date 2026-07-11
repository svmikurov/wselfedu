"""Testing exercise use case."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wse.domain import enums, values
from wse.domain.protocols import Testable

from . import dto
from .abstract import AbstractUseCase
from .protocols import (
    CheckResultDtoProto,
    CheckTestingCommandProto,
    TaskCommandProto,
    Executable,
    HasExerciseAction,
    TaskDtoProto,
)

if TYPE_CHECKING:
    from wse.domain.protocols import (
        Checkable,
        CheckableOption,
        Creatable,
        HasLearnables,
        Repository,
        UniqueLearnable,
    )


class CreateTestingUseCase(
    AbstractUseCase[TaskCommandProto, TaskDtoProto[Testable]]
):
    """Use case for testing task creation."""

    def __init__(
        self,
        learnables_repo: Repository[int, UniqueLearnable],
        service: Creatable[
            HasLearnables[tuple[UniqueLearnable, ...]],
            Testable,
        ],
        task_repo: Repository[str, TaskDtoProto[Testable]],
    ) -> None:
        self._learnables_repo = learnables_repo
        self._task_repo = task_repo
        self._service = service

    def execute(self, cmd: TaskCommandProto) -> TaskDtoProto[Testable]:
        """Create the testing task."""
        learnables = self._learnables_repo.list()
        params = values.TestingParameters(
            option_count=3,
        )

        # TODO: Inject a specification builder
        spec = values.TaskCreating(learnables, params)
        task = self._service.create(spec)
        # TODO: Inject a DTO mapper
        result = dto.Task(task=task, session_id=cmd.session_id)

        self._task_repo.add(result)
        return result


class CheckTestingUseCase(
    AbstractUseCase[CheckTestingCommandProto, CheckResultDtoProto]
):
    """Use case for testing answer check."""

    def __init__(
        self,
        repo: Repository[str, TaskDtoProto[Testable]],
        service: Checkable[CheckableOption, CheckResultDtoProto],
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
        return result


class ExerciseUseCaseStrategy(
    AbstractUseCase[TaskCommandProto, object],
):
    """Use case strategy for exercise action."""

    def __init__(
        self,
        use_case_registry: dict[enums.ExerciseAction, Executable[Any, Any]],
    ) -> None:
        self._use_case_registry = use_case_registry

    def execute(self, cmd: HasExerciseAction) -> object:
        """Execute exercise."""
        use_case = self._use_case_registry[cmd.exercise_action]
        result = use_case.execute(cmd)
        return result
