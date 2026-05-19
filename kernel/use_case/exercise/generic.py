"""Exercise use case."""

from typing import Generic, TypeVar, override

from apps.core.exceptions.storage import StorageMissError
from apps.users.models.user import Person
from ports.abstract.use_case import AbstractUseCase
from ports.contract.entity.domain.exercise import (
    HasExerciseAction,
    HasExerciseStatus,
)
from ports.contract.entity.domain.params import HasConfig
from ports.contract.enums import ExerciseAction, ExerciseStatus
from ports.contract.infra.builder import TaskBuilderProtocol
from ports.contract.infra.resolver import ResolverProtocol
from ports.contract.infra.service import UserSpecServiceProtocol
from ports.contract.infra.spec import ExerciseSpecFactoryProtocol
from ports.contract.infra.storage.general import CommandStorageProtocol
from ports.interfaces.protocols.command.assembler import (
    UserDataCommandProtocol,
)
from ports.interfaces.protocols.domain.exercise import (
    ExerciseConfigProtocol,
    ExerciseParametersProtocol,
)
from ports.interfaces.protocols.service.exercise import ExerciseCaseProtocol
from utils.audit.base import BaseAuditable
from utils.audit.protocol import AuditorProtocol

CommandT = UserDataCommandProtocol[HasExerciseAction]
ParamsT = TypeVar('ParamsT', bound=ExerciseParametersProtocol)
SpecT = TypeVar('SpecT', bound=HasConfig[ExerciseConfigProtocol])
DomainT = TypeVar('DomainT', bound=HasExerciseStatus)
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
            ExerciseAction,
            ExerciseSpecFactoryProtocol[
                CommandT, ParamsT, DomainT | None, SpecT
            ],
        ],
        service_registry: dict[
            ExerciseAction,
            UserSpecServiceProtocol[
                SpecT,
                ExerciseCaseProtocol[DomainT, ResultT],
            ],
        ],
        builder_registry: dict[
            ExerciseStatus,
            TaskBuilderProtocol[
                HasExerciseStatus,
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
        action = self._get_initial_action(command)

        # Exercise has "create", "perform", and "display" parameters.
        params = self._resolve_params(command)

        # Action type specification is built using command and exercise
        # parameters.
        spec = self._build_spec(command, params, action)

        case = self._execute_service(command.user, spec, action)

        if case.status == ExerciseStatus.NEW_TASK:
            self._storage.save(command, case.domain, self._prefix)

        return self._build_result(case, spec)

    def _get_initial_action(self, command: CommandT) -> ExerciseAction:
        return command.data.action

    def _resolve_params(self, command: CommandT) -> ParamsT:
        self.auditor.record('config_resolver.call', obj=self._config_resolver)
        params = self._config_resolver.resolve(command)
        self.auditor.record('config_resolver.ok', parameters=params)
        return params

    def _build_spec(
        self,
        command: CommandT,
        params: ParamsT,
        action: ExerciseAction,
    ) -> SpecT:
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
        return spec

    def _execute_service(
        self,
        user: Person,
        spec: SpecT,
        action: ExerciseAction,
    ) -> ExerciseCaseProtocol[DomainT, ResultT]:
        service = self._service_registry[action]
        self.auditor.record('selected_service.call', obj=service, spec=spec)
        case = service.execute(user, spec)
        self.auditor.record('selected_service.ok', case=case)
        return case

    def _build_result(
        self,
        case: ExerciseCaseProtocol[DomainT, ResultT],
        spec: SpecT,
    ) -> ResultT:
        builder = self._builder_registry[case.status]
        result = builder.build(case, spec)
        self.auditor.record('exercise_build.ok', obj=builder)
        return result
