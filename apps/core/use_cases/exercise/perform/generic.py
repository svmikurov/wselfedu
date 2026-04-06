"""Detail exercise use case."""

from typing import Generic, Protocol, TypeVar, override

from apps.core.adapters.command.protocol import CompositeAdapterProtocol
from apps.core.assemblers.protocol import UserDataCommandProtocol
from apps.core.domains.exercise.enums import ExerciseProcessEnum
from apps.core.domains.exercise.protocol import HasExerciseConditions
from apps.core.factories.protocol import CaseFactoryProtocol
from apps.core.services.protocol import ServiceProtocol
from apps.core.storages.services.iabc import AbstractCommandStorage
from apps.core.use_cases.abstract import AbstractUseCase
from apps.core.use_cases.protocol import ResolverProtocol
from apps.core.validators.request.protocol import ExerciseProcessAction


class ExerciseConditions(Protocol):
    """Exercise conditions."""


ParamsT = TypeVar('ParamsT', bound=HasExerciseConditions[ExerciseConditions])
SpecT = TypeVar('SpecT')
CaseT = TypeVar('CaseT')
TaskT = TypeVar('TaskT')


class ExerciseUseCase(
    AbstractUseCase[
        UserDataCommandProtocol[ExerciseProcessAction],
        TaskT,
    ],
    Generic[ParamsT, SpecT, CaseT, TaskT],
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
            ExerciseProcessEnum,
            CaseFactoryProtocol[ParamsT, CaseT, TaskT],
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
    ) -> TaskT:
        """Start stored exercise."""
        # Get dependencies
        action = command.data['action']
        adapter = self._adapter_registry[action]
        service = self._service_registry[action]
        factory = self._factory_registry[action]

        # Get data
        parameters = self._config_resolver.resolve(command)
        retrieved_case = self._storage.retrieve(command, self._store_prefix)

        # Execute
        spec = adapter.adapt(command, parameters, retrieved_case)
        case = service.execute(command.user, spec)
        task = factory.build(parameters, case)

        self._storage.save(command, case, self._store_prefix)
        return task
