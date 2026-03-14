"""Core exercise domain."""

from typing import TypeVar

from apps.core.domains.exercise.types import CheckResultProtocol
from apps.core.domains.null import NullDTO
from apps.core.handlers.protocol import (
    NullDataProtocol,
    QueryRequestParamsProtocol,
    RequestContextProtocol,
)
from apps.core.services.exercise.abstract import (
    AbstractExerciseCheck,
    AbstractExerciseExplain,
    AbstractMilestone,
    AbstractRegularExerciseCreate,
)
from apps.core.storages.services.iabc import AbstractUserStorage

from ..abstract import AbstractUseCase

# Use case type vars
RequestParams = TypeVar('RequestParams')
RequestContext = TypeVar('RequestContext')
Validated = TypeVar('Validated')
ResultData = TypeVar('ResultData')

# Exercise type vars
Conditions = TypeVar('Conditions')
Case = TypeVar('Case')
CaseMeta = TypeVar('CaseMeta')
UserAnswer = TypeVar('UserAnswer')
CheckResult = TypeVar('CheckResult', bound=CheckResultProtocol)


class RegularCreateExerciseUseCase(
    AbstractUseCase[
        QueryRequestParamsProtocol,
        RequestContextProtocol,
        NullDataProtocol,
        ResultData,
    ],
):
    """Start regular exercise use case."""

    def __init__(
        self,
        store_prefix: str,
        service: AbstractRegularExerciseCreate[
            QueryRequestParamsProtocol,
            tuple[ResultData, CaseMeta],
        ],
        storage: AbstractUserStorage[CaseMeta],
    ) -> None:
        """Construct the use case."""
        self._store_prefix = store_prefix
        self._service = service
        self._storage = storage

    def execute(
        self,
        params: QueryRequestParamsProtocol,
        context: RequestContextProtocol,
        validated: NullDataProtocol,
    ) -> ResultData:
        """Start regular exercise."""
        case, meta = self._service.execute(params)
        self._storage.save(meta, context.user.pk, self._store_prefix)
        return case


class RegularCheckExerciseUseCase(
    AbstractUseCase[
        QueryRequestParamsProtocol,
        RequestContextProtocol,
        UserAnswer,
        ResultData,
    ],
):
    """Regular exercise check use case."""

    def __init__(
        self,
        store_prefix: str,
        storage: AbstractUserStorage[CaseMeta],
        check_service: AbstractExerciseCheck[
            UserAnswer,
            CaseMeta,
            CheckResult,
        ],
        milestone_service: AbstractMilestone[CheckResult, CaseMeta] | None,
        create_use_case: AbstractUseCase[
            QueryRequestParamsProtocol,
            RequestContextProtocol,
            NullDataProtocol,
            ResultData,
        ],
        explain_service: AbstractExerciseExplain[
            UserAnswer,
            CaseMeta,
            ResultData,
        ],
    ) -> None:
        """Construct the use case."""
        self._store_prefix = store_prefix
        self._storage = storage
        self._check_service = check_service
        self._milestone_service = milestone_service
        self._create_use_case = create_use_case
        self._explain_service = explain_service

    def execute(
        self,
        params: QueryRequestParamsProtocol,
        context: RequestContextProtocol,
        validated: UserAnswer,
    ) -> ResultData:
        """Check regular exercise."""
        meta = self._storage.retrieve(context.user.pk, self._store_prefix)
        result = self._check_service.execute(validated, meta)

        if self._milestone_service:
            self._milestone_service.execute(context.user, result, meta)

        if result.is_correct:
            return self._create_use_case.execute(params, context, NullDTO())
        else:
            return self._explain_service.execute(validated, meta)
