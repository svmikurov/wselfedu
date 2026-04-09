"""Detail exercise use case."""

from typing import Generic, Protocol, TypeVar, override

from apps.core.adapters.command.protocol import CompositeAdapterProtocol
from apps.core.assemblers.protocol import UserDataCommandProtocol
from apps.core.domains.exercise.enums import (
    ExerciseProcessEnum,
    ExerciseStatusEnum,
)
from apps.core.domains.exercise.protocol import HasExerciseStatus
from apps.core.domains.task.protocol import TaskBuilderProtocol
from apps.core.services.protocol import ServiceProtocol
from apps.core.storages.services.iabc import AbstractCommandStorage
from apps.core.use_cases.abstract import AbstractUseCase
from apps.core.use_cases.protocol import (
    ExerciseConfig,
    ExerciseParameters,
    ResolverProtocol,
)
from apps.core.validators.request.protocol import ExerciseProcessAction


class ExerciseConditions(Protocol):
    """Exercise conditions."""


ParamsT = TypeVar('ParamsT')
SpecT = TypeVar('SpecT', bound=ExerciseParameters)
CaseT = TypeVar('CaseT', bound=HasExerciseStatus)
ResultT = TypeVar('ResultT')


class ExerciseUseCase(
    AbstractUseCase[
        UserDataCommandProtocol[ExerciseProcessAction],
        ResultT,
    ],
    Generic[ParamsT, SpecT, CaseT, ResultT],
):
    """Process exercise use case."""

    def __init__(
        self,
        store_prefix: str,
        storage: AbstractCommandStorage[
            UserDataCommandProtocol[ExerciseProcessAction],
            CaseT,
        ],
        config_resolver: ResolverProtocol[
            UserDataCommandProtocol[ExerciseProcessAction],
            ParamsT,
        ],
        adapter_registry: dict[
            ExerciseProcessEnum,
            CompositeAdapterProtocol[
                UserDataCommandProtocol[ExerciseProcessAction],
                ParamsT,
                CaseT,
                SpecT,
            ],
        ],
        service_registry: dict[
            ExerciseProcessEnum,
            ServiceProtocol[SpecT, CaseT],
        ],
        factory_registry: dict[
            ExerciseStatusEnum,
            TaskBuilderProtocol[
                CaseT,
                ExerciseConfig,
                ResultT,
            ],
        ],
    ) -> None:
        """Construct the use case."""
        self._store_prefix = store_prefix
        self._storage = storage
        self._config_resolver = config_resolver
        self._adapter_registry = adapter_registry
        self._service_registry = service_registry
        self._factory_registry = factory_registry

    @override
    def execute(
        self,
        command: UserDataCommandProtocol[ExerciseProcessAction],
    ) -> ResultT:
        """Start stored exercise."""
        action = command.data['action']
        adapter = self._adapter_registry[action]
        service = self._service_registry[action]

        # Prepare arguments
        # -----------------
        parameters = self._config_resolver.resolve(command)
        # Saved case contains item's study data that uses
        # for exercise check, to update item's study progress
        # and other exercise case process.
        retrieved_case = self._storage.retrieve(command, self._store_prefix)
        spec = adapter.adapt(command, parameters, retrieved_case)

        # Execute
        # -------
        case = service.execute(command.user, spec)

        # Handle result
        # -------------
        factory = self._factory_registry[case.status]
        result = factory.build(case, spec.conf)
        self._storage.save(command, case, self._store_prefix)
        return result
