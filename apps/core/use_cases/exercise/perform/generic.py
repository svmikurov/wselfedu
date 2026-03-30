"""Detail exercise use case."""

from typing import Protocol, TypeVar, override, Generic

from apps.core.adapters.command.protocol import CompositeAdapterProtocol
from apps.core.assemblers.protocol import UserDataCommandProtocol
from apps.core.domains.exercise.enums import ExerciseProcessEnum
from apps.core.domains.exercise.protocol import HasExerciseConditions
from apps.core.factories.abstract import AbstractExerciseDTOFactory
from apps.core.services.protocol import ServiceProtocol
from apps.core.storages.services.iabc import AbstractCommandStorage
from apps.core.use_cases.abstract import AbstractUseCase
from apps.core.use_cases.protocol import ResolverProtocol
from apps.core.validators.request.protocol import ExerciseProcessAction


class ExerciseConditions(Protocol):
    """Exercise conditions."""


ExerciseParamsT = TypeVar(
    'ExerciseParamsT',
    bound=HasExerciseConditions[ExerciseConditions],
)
SpecT = TypeVar('SpecT')
CaseT = TypeVar('CaseT')
CaseMetaT = TypeVar('CaseMetaT')
ResultT = TypeVar('ResultT')


class ExerciseUseCase(
    AbstractUseCase[
        UserDataCommandProtocol[ExerciseProcessAction],
        ResultT,
    ],
    Generic[
        ExerciseParamsT,
        SpecT,
        CaseT,
        CaseMetaT,
        ResultT,
    ],
):
    """Process exercise use case."""

    def __init__(
        self,
        store_prefix: str,
        storage: AbstractCommandStorage[
            UserDataCommandProtocol[ExerciseProcessAction],
            CaseMetaT,
        ],
        config_resolver: ResolverProtocol[
            UserDataCommandProtocol[ExerciseProcessAction],
            ExerciseParamsT,
        ],
        adapter_registry: dict[
            ExerciseProcessEnum,
            CompositeAdapterProtocol[
                UserDataCommandProtocol[ExerciseProcessAction],
                ExerciseParamsT,
                CaseMetaT,
                SpecT,
            ],
        ],
        service_registry: dict[
            ExerciseProcessEnum,
            ServiceProtocol[
                SpecT,
                tuple[CaseT, CaseMetaT],
            ],
        ],
        factory_registry: dict[
            ExerciseProcessEnum,
            AbstractExerciseDTOFactory[
                CaseT,
                ExerciseParamsT,
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
        # Get dependencies
        action = command.data['action']
        adapter = self._adapter_registry[action]
        service = self._service_registry[action]
        factory = self._factory_registry[action]

        # Prepare data
        parameters = self._config_resolver.resolve(command)
        retrieved_meta = self._storage.retrieve(command, self._store_prefix)
        spec = adapter.adapt(command, parameters, retrieved_meta)

        # Execute
        case, new_meta = service.execute(command.user, spec)

        # Prepare result
        result = factory.build(case, parameters)
        self._storage.save(command, new_meta, self._store_prefix)

        return result
