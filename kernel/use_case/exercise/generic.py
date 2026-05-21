"""Exercise use case."""

from typing import Generic, TypeVar, override

from apps.core.exceptions.storage import StorageMissError
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
        # Exercise has "create", "perform", and "display" parameters.
        params = self._resolve_params(command)
        # Case may not exist (exercise not started yet).
        stored = self._get_stored(command)
        current_cmd = command

        while True:
            spec = self._build_spec(current_cmd, params, stored)
            case = self._execute_service(current_cmd, spec)
            next_action = self._get_next_action(case)

            if case.status == ExerciseStatus.NEW_TASK:
                self._save_domain_result(current_cmd, case.domain)

            if next_action:
                current_cmd = self._get_next_command(current_cmd, next_action)
            else:
                return self._build_result(case, spec)

    # =============================================
    # Utility methods
    # =============================================

    def _save_domain_result(self, command: CommandT, domain: DomainT) -> None:
        self._storage.save(command, domain, self._prefix)

    def _get_action(self, command: CommandT) -> ExerciseAction:
        return command.data.action

    def _resolve_params(self, command: CommandT) -> ParamsT:
        self.auditor.record('config_resolver.call', obj=self._config_resolver)
        params = self._config_resolver.resolve(command)
        self.auditor.record('config_resolver.ok', parameters=params)
        return params

    def _get_stored(self, command: CommandT) -> DomainT | None:
        # StorageMissError is expected flow, not an exceptional error.
        try:
            return self._storage.retrieve(command, self._prefix)
        except StorageMissError:
            return None

    def _build_spec(
        self,
        command: CommandT,
        params: ParamsT,
        stored: DomainT | None,
    ) -> SpecT:
        spec_factory = self._spec_factory_registry[self._get_action(command)]
        self.auditor.record(
            'spec_factory.select',
            obj=spec_factory,
            command=command,
            params=params,
            stored=stored,
        )
        spec = spec_factory.create(command, params, stored)
        self.auditor.record('service_spec.created', spec=spec)
        return spec

    def _execute_service(
        self,
        command: CommandT,
        spec: SpecT,
    ) -> ExerciseCaseProtocol[DomainT, ResultT]:
        service = self._service_registry[self._get_action(command)]
        self.auditor.record('selected_service.call', obj=service, spec=spec)
        case = service.execute(command.user, spec)
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

    # =============================================
    # Workflow loop methods
    # =============================================

    # TODO: Add milestone action
    def _get_next_action(
        self,
        case: ExerciseCaseProtocol[DomainT, ResultT],
    ) -> ExerciseAction | None:
        action: ExerciseAction | None

        match case.status:
            case ExerciseStatus.CORRECT:
                action = ExerciseAction.CREATE_TASK
            case ExerciseStatus.WRONG:
                action = ExerciseAction.EXPLAIN_TASK
            case _:
                action = None

        self.auditor.record(f'nex_action.{action or "no_action_to_execute"}')
        return action

    def _get_next_command(
        self,
        command: CommandT,
        next_action: ExerciseAction,
    ) -> CommandT:
        return command
