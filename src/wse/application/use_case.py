"""Application use cases."""

from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar, override

from wse.domain import enums
from wse.domain.protocols import CheckableOption, HasCorrect, Testable
from wse.domain.values import AnswerCheck

from .abstract import (
    AbstractCheckAnswerUseCase,
    AbstractCreateTaskUseCase,
    AbstractExerciseUseCase,
)
from .dto import ExerciseResult

if TYPE_CHECKING:
    from wse.domain.protocols import (
        AnswerCheckableService,
        CandidatesRepositoryProtocol,
        CreateTaskServiceProtocol,
        EventProto,
        ExerciseCommandProto,
    )

T = TypeVar('T')


class CreateTaskUseCase(AbstractCreateTaskUseCase[T], Generic[T]):
    """Create task use case."""

    def __init__(
        self,
        repository: CandidatesRepositoryProtocol,
        domain: CreateTaskServiceProtocol[T],
    ) -> None:
        self._repository = repository
        self._domain = domain

    @override
    def execute(self) -> T:
        """Create the task."""
        candidates = self._repository.list()
        return self._domain.execute(candidates)


class CheckAnswerUseCase(
    AbstractCheckAnswerUseCase[CheckableOption, HasCorrect],
):
    """Use case for check th user answer."""

    def __init__(
        self,
        domain: AnswerCheckableService[CheckableOption, HasCorrect],
    ) -> None:
        self._domain = domain

    @override
    def execute(self, spec: CheckableOption) -> HasCorrect:
        return self._domain.execute(spec)


# IDEA: Testing exercise process use case
class ExerciseProcessor(AbstractExerciseUseCase):
    """Testing execute use case."""

    __test__ = False

    def __init__(
        self,
        use_case_to_create: AbstractCreateTaskUseCase[Testable],
        use_case_to_check: AbstractCheckAnswerUseCase[
            CheckableOption, HasCorrect
        ],
    ) -> None:
        self._use_case_to_create = use_case_to_create
        self._use_case_to_check = use_case_to_check

    def execute(
        self,
        command: ExerciseCommandProto,
    ) -> EventProto:
        """Execute exercise command action."""
        # HACK: Temporary persistent answer check object
        answer_check = AnswerCheck(3, 3)

        match command.action:
            case enums.ExerciseAction.CREATE_TASK:
                return ExerciseResult(
                    task=self._use_case_to_create.execute(),
                )
            case enums.ExerciseAction.CHECK_ANSWER:
                return self._use_case_to_check.execute(
                    spec=answer_check,
                )
            case _:
                raise ValueError
