"""Exercise use case."""

from typing import Generic, TypeVar, override

from apps.core.exceptions.storage import StorageMissError
from apps.core.resolvers.protocol import ResolverProtocol
from apps.core.services.protocol import UserServiceProtocol
from apps.core.storages.services.protocol import CommandStorageProtocol
from apps.core.use_cases.abstract import AbstractUseCase
from contracts.entity.domain import params
from contracts.entity.domain.exercise import flow
from contracts.entity.domain.exercise.fields import HasExerciseAction
from interfaces.protocols.domain.exercise import (
    ExerciseConfigProtocol,
    ExerciseParametersProtocol,
)
from ports.contract import enums
from ports.contract.entity.command import UserDataCommandProtocol
from ports.contract.infra.builder import TaskBuilderProtocol
from ports.contract.infra.spec import ExerciseSpecFactoryProtocol
from utils.audit.base import BaseAuditable
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
        spec_factory_registry: dict[
            enums.ExerciseAction,
            ExerciseSpecFactoryProtocol[
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
        self._spec_factory_registry = spec_factory_registry
        self._service_registry = service_registry
        self._builder_registry = builder_registry

    @override
    def execute(self, command: CommandT) -> ResultT:
        """Process exercise."""
        # Handled use cases: "create", "check",
        # "update progress", and other actions.
        # Each action is bound to a stored exercise case that has
        # a hash key derived from the username and storage prefix.
        action = command.data.action

        # Exercise has "create", "perform", and "display" parameters.
        self.auditor.record('config_resolver.call', obj=self._config_resolver)
        params = self._config_resolver.resolve(command)
        self.auditor.record('config_resolver.ok', parameters=params)

        # Action type specification is built using command and exercise
        # parameters.
        spec_factory = self._spec_factory_registry[action]
        self.auditor.record('spec_factory.select', obj=spec_factory)
        # Case may not exist (not started yet).
        # StorageMissError is expected flow, not an exceptional error.
        try:
            stored = self._storage.retrieve(command, self._prefix)
        except StorageMissError:
            self.auditor.record('spec_factory.call', params=params)
            spec = spec_factory.create(command, params, None)
        else:
            self.auditor.record(
                'spec_factory.call', params=params, stored=stored
            )
            spec = spec_factory.create(command, params, stored)
        self.auditor.record('service_spec.created', spec=spec)

        service = self._service_registry[action]
        self.auditor.record('selected_service.call', obj=service, spec=spec)
        case = service.execute(command.user, spec)
        self.auditor.record('selected_service.ok', case=case)

        if case.status == enums.ExerciseStatus.NEW_TASK:
            self._storage.save(command, case.domain, self._prefix)

        builder = self._builder_registry[case.status]
        result = builder.build(case, spec)
        self.auditor.record('exercise_build.ok', obj=builder)
        return result
