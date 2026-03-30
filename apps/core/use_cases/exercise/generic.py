"""Detail exercise use case."""

from typing import Generic, TypeVar, override

from apps.core.assemblers.protocol import (
    UserCommandProtocol,
    UserDataCommandProtocol,
)
from apps.core.domains.exercise.protocol import (
    HasCheckResult,
    HasExerciseConditions,
)
from apps.core.factories.abstract import AbstractExerciseDTOFactory
from apps.core.services.exercise.abstract import (
    AbstractCheckExerciseService,
    AbstractCreateExerciseService,
    AbstractExplainExerciseService,
    AbstractMilestoneService,
)
from apps.core.storages.services.iabc import AbstractCommandStorage
from apps.core.use_cases.abstract import AbstractUseCase
from apps.core.use_cases.protocol import ExerciseConfigurationResolverProtocol

ValidatedCommandData = TypeVar('ValidatedCommandData')

Case = TypeVar('Case')
CaseMeta = TypeVar('CaseMeta')
CheckResult = TypeVar('CheckResult', bound=HasCheckResult)

ExerciseParameters = TypeVar('ExerciseParameters', bound=HasExerciseConditions)
ResultData = TypeVar('ResultData')


class StartExerciseUseCase(
    AbstractUseCase[
        UserCommandProtocol,
        tuple[Case, CaseMeta],
    ],
):
    """Authenticated user exercise start use case.

    Parameters
    ----------
    config_resolver :
        Exercise perform parameters repository.
    service :
        Start exercise service.
    store_prefix :
        Store prefix for created exercise meta data.
    storage :
        Storage to store created exercise meta data.
    dto_factory :
        Use case result DTO factory.

    """

    def __init__(
        self,
        config_resolver: ExerciseConfigurationResolverProtocol[
            UserCommandProtocol,
            ExerciseParameters,
        ],
        service: AbstractCreateExerciseService[
            ExerciseParameters,
            Case,
            CaseMeta,
        ],
        store_prefix: str,
        storage: AbstractCommandStorage[CaseMeta, UserCommandProtocol],
        dto_factory: AbstractExerciseDTOFactory[
            Case,
            ExerciseParameters,
            tuple[Case, CaseMeta],
        ],
    ) -> None:
        """Construct the use case."""
        self._store_prefix = store_prefix
        self._storage = storage
        self._config_resolver = config_resolver
        self._service = service
        self._dto_factory = dto_factory

    @override
    def execute(
        self,
        command: UserCommandProtocol,
    ) -> tuple[Case, CaseMeta]:
        """Start stored exercise."""
        parameters = self._config_resolver.resolve(command)
        case, meta = self._service.execute(parameters, command.user)
        self._storage.save(meta, command, self._store_prefix)
        result = self._dto_factory.build(case, parameters)
        return result


class CheckExerciseUseCase(
    AbstractUseCase[
        UserDataCommandProtocol[ValidatedCommandData],
        ResultData,
    ],
    Generic[ValidatedCommandData, ResultData],
):
    """Exercise check use case.

    Parameters
    ----------
    store_prefix :
        Store prefix for created exercise meta data.
    storage :
        Storage to store created exercise meta data.
    check_service :
        Check exercise service.
    config_resolver :
        Exercise perform parameters repository.
    milestone_service :
        ...
    create_use_case :
        ...
    explain_service :
        ...

    """

    def __init__(
        self,
        store_prefix: str,
        storage: AbstractCommandStorage[CaseMeta, UserCommandProtocol],
        check_service: AbstractCheckExerciseService[
            ValidatedCommandData,
            CaseMeta,
            CheckResult,
        ],
        config_resolver: ExerciseConfigurationResolverProtocol[
            UserCommandProtocol,
            ExerciseParameters,
        ],
        milestone_service: AbstractMilestoneService[
            UserDataCommandProtocol[ValidatedCommandData],
            CaseMeta,
            CheckResult,
            ExerciseParameters,
        ]
        | None,
        create_use_case: AbstractUseCase[
            UserDataCommandProtocol[ValidatedCommandData],
            ResultData,
        ],
        explain_service: AbstractExplainExerciseService[
            UserDataCommandProtocol[ValidatedCommandData],
            CaseMeta,
            ResultData,
        ],
    ) -> None:
        """Construct the use case."""
        self._store_prefix = store_prefix
        self._storage = storage
        self._check_service = check_service
        self._config_resolver = config_resolver
        self._milestone_service = milestone_service
        self._create_use_case = create_use_case
        self._explain_service = explain_service

    @override
    def execute(
        self,
        command: UserDataCommandProtocol[ValidatedCommandData],
    ) -> ResultData:
        """Check student's exercise solution."""
        # Stored (cached) exercise case metadata contains
        # correct answer on current exercise case.
        meta = self._storage.retrieve(command, self._store_prefix)
        result = self._check_service.execute(command.data, meta)

        # Stored (cached) exercise parameters contains
        # exercise availability and milestone data to update.
        exercise_parameters = self._config_resolver.resolve(command)

        if self._milestone_service:
            self._milestone_service.execute(
                command,
                meta,
                result,
                exercise_parameters,
            )

        if result.is_correct:
            return self._create_use_case.execute(command)
        else:
            return self._explain_service.execute(command, meta)


class ProcessExerciseUseCase(
    AbstractUseCase[
        UserDataCommandProtocol[ValidatedCommandData],
        ResultData,
    ],
    Generic[ValidatedCommandData, ResultData],
):
    """Process exercise performing the use case."""

    def __init__(
        self,
        # FIXME: Fix object type hint
        strategy: object,
    ) -> None:
        """Construct the handler."""
        self._strategy = strategy

    def execute(
        self,
        command: UserDataCommandProtocol[ValidatedCommandData],
    ) -> ResultData:
        """Execute."""
        # TODO: Implement `execute(...)` method
        return super().execute(command)
