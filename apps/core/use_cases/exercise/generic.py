"""Exercise use case."""

from typing import Generic, TypeVar, override

from apps.core.adapters.exercise.protocol import ExerciseProcessAdapterProtocol
from apps.core.assemblers.protocol import UserDataCommandProtocol
from apps.core.domains.exercise.enums import (
    ExerciseProcessEnum,
    ExerciseStatusEnum,
)
from apps.core.domains.exercise.protocol import HasExerciseStatus
from apps.core.domains.task.protocol import TaskBuilderProtocol
from apps.core.exceptions.storage import CacheMissError
from apps.core.services.protocol import ServiceProtocol
from apps.core.storages.services.iabc import AbstractCommandStorage
from apps.core.use_cases.abstract import AbstractUseCase
from apps.core.use_cases.protocol import (
    ExerciseConfig,
    ExerciseParameters,
    ResolverProtocol,
)
from apps.core.validators.request.protocol import HasExerciseProcessAction

ParamsT = TypeVar('ParamsT')
SpecT = TypeVar('SpecT', bound=ExerciseParameters)
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
        storage: AbstractCommandStorage[CommandT, CaseT],
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
            TaskBuilderProtocol[CaseT, ExerciseConfig, ResultT],
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

        # Prepare arguments
        # -----------------
        parameters = self._config_resolver.resolve(command)
        # Saved case contains item's study data that uses
        # for exercise check, to update item's study progress
        # and other exercise case process.
        try:
            retrieved_case = self._storage.retrieve(command, self._prefix)
        except CacheMissError:
            retrieved_case = None
        spec = adapter.adapt(command, parameters, retrieved_case)

        # Execute
        # -------
        case = service.execute(command.user, spec)

        # Handle result
        # -------------
        builder = self._builder_registry[case.status]
        result = builder.build(case, spec.conf)
        self._storage.save(command, case, self._prefix)
        return result
