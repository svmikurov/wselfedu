"""Exercise use case."""

from typing import Generic, TypeVar, override

from apps.core.adapters.exercise.protocol import ExerciseProcessAdapterProtocol
from apps.core.assemblers.protocol import UserDataCommandProtocol
from apps.core.domains.exercise.protocol import (
    ExerciseConfigProtocol,
    ExerciseParametersProtocol,
    HasExerciseAction,
)
from apps.core.domains.task.protocol import TaskBuilderProtocol
from apps.core.exceptions.storage import StorageMissError
from apps.core.resolvers.protocol import ResolverProtocol
from apps.core.services.protocol import UserServiceProtocol
from apps.core.storages.services.protocol import CommandStorageProtocol
from apps.core.use_cases.abstract import AbstractUseCase
from contracts import enums
from contracts.entity.domain import params
from contracts.entity.domain.exercise import flow
from utils.audit.mixins import BaseAuditable
from utils.audit.protocol import AuditorProtocol

CommandT = UserDataCommandProtocol[HasExerciseAction]
ParamsT = TypeVar('ParamsT', bound=ExerciseParametersProtocol)
SpecT = TypeVar('SpecT', bound=params.HasConfig[ExerciseConfigProtocol])
DomainT = TypeVar('DomainT', bound=flow.ExerciseDomainResultProtocol)
ResultT = TypeVar('ResultT')


class ExerciseUseCaseStrategy(
    BaseAuditable,
    AbstractUseCase[CommandT, ResultT],
    Generic[ParamsT, SpecT, DomainT, ResultT],
):
    """Process exercise use case."""

    def __init__(
        self,
        prefix: str,
        storage: CommandStorageProtocol[
            CommandT,
            DomainT,
        ],
        config_resolver: ResolverProtocol[CommandT, ParamsT],
        adapter_registry: dict[
            enums.ExerciseAction,
            ExerciseProcessAdapterProtocol[
                CommandT, ParamsT, DomainT | None, SpecT
            ],
        ],
        service_registry: dict[
            enums.ExerciseAction,
            UserServiceProtocol[
                SpecT,
                flow.ExerciseCaseProtocol[DomainT],
            ],
        ],
        builder_registry: dict[
            enums.ExerciseStatus,
            TaskBuilderProtocol[
                flow.ExerciseCaseProtocol[DomainT],
                SpecT,
                ResultT,
            ],
        ],
        name: str | None = None,
        auditor: AuditorProtocol | None = None,
    ) -> None:
        """Construct the use case."""
        super().__init__(name=name, auditor=auditor)
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
        self.auditor.record('adapter_strategy.select', obj=adapter)

        service = self._service_registry[action]
        self.auditor.record('service_strategy.select', obj=service)

        self.auditor.record('config_resolver.call', obj=self._config_resolver)
        parameters = self._config_resolver.resolve(command)
        self.auditor.record('config_resolver.ok', parameters=parameters)

        # Case may not exist (not started yet)
        # StorageMissError is expected flow, not an exceptional error
        try:
            existing_domain = self._storage.retrieve(command, self._prefix)
        except StorageMissError:
            spec = adapter.adapt(command, parameters, None)
        else:
            spec = adapter.adapt(command, parameters, existing_domain)

        case = service.execute(command.user, spec)

        if case.status == enums.ExerciseStatus.NEW_TASK:
            self._storage.save(command, case.domain, self._prefix)

        builder = self._builder_registry[case.status]
        result = builder.build(case, spec)
        self.auditor.record('exercise_build.ok', obj=builder)
        return result
