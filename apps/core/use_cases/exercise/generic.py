"""Exercise use case."""

from typing import Generic, TypeVar, override

from apps.core.adapters.exercise.protocol import ExerciseProcessAdapterProtocol
from apps.core.assemblers.protocol import UserDataCommandProtocol
from apps.core.domains.exercise.enums import (
    ExerciseProcessEnum,
    ExerciseStatusEnum,
)
from apps.core.domains.exercise.protocol import (
    ExerciseConfigProtocol,
    ExerciseParametersProtocol,
    HasExerciseConfig,
    HasExerciseStatus,
)
from apps.core.domains.task.protocol import TaskBuilderProtocol
from apps.core.exceptions.storage import StorageMissError
from apps.core.services.protocol import ServiceProtocol
from apps.core.storages.services.protocol import CommandStorageProtocol
from apps.core.use_cases.abstract import AbstractUseCase
from apps.core.validators.request.protocol import HasExerciseProcessAction

from ..protocol import ResolverProtocol

ParamsT = TypeVar('ParamsT', bound=ExerciseParametersProtocol)
SpecT = TypeVar('SpecT', bound=HasExerciseConfig[ExerciseConfigProtocol])
CaseT = TypeVar('CaseT', bound=HasExerciseStatus)
ResultT = TypeVar('ResultT')
CommandT = UserDataCommandProtocol[HasExerciseProcessAction]


class ExerciseUseCaseStrategy(
    AbstractUseCase[CommandT, ResultT],
    Generic[ParamsT, SpecT, CaseT, ResultT],
):
    """Process exercise use case."""

    def __init__(
        self,
        prefix: str,
        storage: CommandStorageProtocol[CommandT, CaseT],
        config_resolver: ResolverProtocol[CommandT, ParamsT],
        adapter_registry: dict[
            ExerciseProcessEnum,
            ExerciseProcessAdapterProtocol[
                CommandT, ParamsT, CaseT | None, SpecT
            ],
        ],
        service_registry: dict[
            ExerciseProcessEnum,
            ServiceProtocol[SpecT, CaseT],
        ],
        builder_registry: dict[
            ExerciseStatusEnum,
            TaskBuilderProtocol[CaseT, ExerciseConfigProtocol, ResultT],
        ],
    ) -> None:
        """Construct the use case."""
        self._prefix = prefix
        self._storage = storage
        self._config_resolver = config_resolver
        self._adapter_registry = adapter_registry
        self._service_registry = service_registry
        self._builder_registry = builder_registry

    @override
    def execute(self, command: CommandT) -> ResultT:
        """Process exercise."""
        action = command.data.action
        adapter = self._adapter_registry[action]
        service = self._service_registry[action]
        parameters = self._config_resolver.resolve(command)

        # Case may not exist (not started yet)
        # StorageMissError is expected flow, not an exceptional error
        try:
            existing_case = self._storage.retrieve(command, self._prefix)
        except StorageMissError:
            spec = adapter.adapt(command, parameters, None)
        else:
            spec = adapter.adapt(command, parameters, existing_case)

        case = service.execute(command.user, spec)

        if case.status == ExerciseStatusEnum.NEW_TASK:
            self._storage.save(command, case, self._prefix)

        builder = self._builder_registry[case.status]
        result = builder.build(case, spec.conf)
        return result
