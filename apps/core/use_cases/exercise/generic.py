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
    ExerciseProcessResultProtocol,
    HasExerciseConfig,
    HasExerciseProcessAction,
)
from apps.core.domains.task.protocol import TaskBuilderProtocol
from apps.core.exceptions.storage import StorageMissError
from apps.core.resolvers.protocol import ResolverProtocol
from apps.core.services.protocol import UserServiceProtocol
from apps.core.storages.services.protocol import CommandStorageProtocol
from apps.core.use_cases.abstract import AbstractUseCase

CommandT = UserDataCommandProtocol[HasExerciseProcessAction]
ParamsT = TypeVar('ParamsT', bound=ExerciseParametersProtocol)
SpecT = TypeVar('SpecT', bound=HasExerciseConfig[ExerciseConfigProtocol])
CaseT = TypeVar('CaseT')
ResultT = TypeVar('ResultT')


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
            UserServiceProtocol[SpecT, ExerciseProcessResultProtocol[CaseT]],
        ],
        builder_registry: dict[
            ExerciseStatusEnum,
            TaskBuilderProtocol[
                ExerciseProcessResultProtocol[CaseT],
                SpecT,
                ResultT,
            ],
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

        domain = service.execute(command.user, spec)

        if domain.status == ExerciseStatusEnum.NEW_TASK:
            self._storage.save(command, domain.case, self._prefix)

        builder = self._builder_registry[domain.status]
        result = builder.build(domain, spec)
        return result
