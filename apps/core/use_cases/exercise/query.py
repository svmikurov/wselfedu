"""Core exercise use case."""

from typing import Generic, TypeVar

from apps.core.assemblers.protocol import (
    UserQueryCommandProtocol,
    UserQueryDataCommandProtocol,
)
from apps.core.domains.exercise.protocol import CheckResultProtocol
from apps.core.services.exercise.abstract import (
    AbstractExerciseCheck,
    AbstractExerciseExplain,
    AbstractMilestone,
    AbstractRegularExerciseCreate,
)
from apps.core.storages.services.iabc import AbstractUserStorage

from ..abstract import AbstractUseCase

QueryType = TypeVar('QueryType')
ResultData = TypeVar('ResultData')
CaseMeta = TypeVar('CaseMeta')
UserAnswer = TypeVar('UserAnswer')
CheckResult = TypeVar('CheckResult', bound=CheckResultProtocol)


class QueryStartExerciseUseCase(
    AbstractUseCase[
        UserQueryCommandProtocol[QueryType],
        ResultData,
    ],
    Generic[QueryType, CaseMeta, ResultData],
):
    """Regular query exercise start use case."""

    def __init__(
        self,
        store_prefix: str,
        storage: AbstractUserStorage[CaseMeta],
        service: AbstractRegularExerciseCreate[
            QueryType,
            tuple[ResultData, CaseMeta],
        ],
    ) -> None:
        """Construct the use case."""
        self._store_prefix = store_prefix
        self._storage = storage
        self._service = service

    def execute(
        self,
        command: UserQueryCommandProtocol[QueryType],
    ) -> ResultData:
        """Start regular exercise."""
        case, meta = self._service.execute(command.query)
        self._storage.save(meta, command.user.pk, self._store_prefix)
        return case


class QueryCheckExerciseUseCase(
    AbstractUseCase[
        UserQueryDataCommandProtocol[QueryType, UserAnswer],
        ResultData,
    ],
    Generic[QueryType, UserAnswer, CaseMeta, CheckResult, ResultData],
):
    """Regular query exercise check use case."""

    def __init__(
        self,
        store_prefix: str,
        storage: AbstractUserStorage[CaseMeta],
        check_service: AbstractExerciseCheck[
            UserAnswer,
            CaseMeta,
            CheckResult,
        ],
        explain_service: AbstractExerciseExplain[
            UserAnswer,
            CaseMeta,
            ResultData,
        ],
        milestone_service: AbstractMilestone[CheckResult, CaseMeta] | None,
        create_use_case: AbstractUseCase[
            UserQueryCommandProtocol[QueryType],
            ResultData,
        ],
    ) -> None:
        """Construct the use case."""
        self._store_prefix = store_prefix
        self._storage = storage
        self._check_service = check_service
        self._explain_service = explain_service
        self._milestone_service = milestone_service
        self._create_use_case = create_use_case

    def execute(
        self,
        command: UserQueryDataCommandProtocol[QueryType, UserAnswer],
    ) -> ResultData:
        """Check regular exercise."""
        meta = self._storage.retrieve(command.user.pk, self._store_prefix)
        result = self._check_service.execute(command.data, meta)

        if self._milestone_service:
            self._milestone_service.execute(command.user, result, meta)

        if result.is_correct:
            return self._create_use_case.execute(command)
        else:
            return self._explain_service.execute(command.data, meta)
