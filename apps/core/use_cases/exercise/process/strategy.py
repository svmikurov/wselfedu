"""Process study progress update use case."""

from typing import Generic, TypeVar, override

from apps.core.adapters.command.protocol import CompositeAdapterProtocol
from apps.core.assemblers.protocol import (
    UserCommandProtocol,
    UserDataCommandProtocol,
)
from apps.core.domains.exercise.enums import ExerciseProcessEnum
from apps.core.domains.exercise.protocol import HasExerciseStatus
from apps.core.services.exercise.protocol import HasRepositoryUserCommand
from apps.core.services.protocol import ServiceProtocol
from apps.core.storages.services.iabc import AbstractCommandStorage
from apps.core.use_cases.abstract import AbstractUseCase
from apps.core.validators.request.protocol import ExerciseProcessAction

CaseMeta = TypeVar('CaseMeta')
ExerciseParameters = TypeVar('ExerciseParameters')
Filter = TypeVar('Filter')
Updates = TypeVar('Updates')


class ProcessExerciseStrategy(
    AbstractUseCase[
        UserDataCommandProtocol[ExerciseProcessAction],
        HasExerciseStatus,
    ],
    Generic[CaseMeta, Filter, Updates],
):
    """Process exercise strategy."""

    def __init__(
        self,
        store_prefix: str,
        storage: AbstractCommandStorage[CaseMeta, UserCommandProtocol],
        adapter_registry: dict[
            ExerciseProcessEnum,
            CompositeAdapterProtocol[
                UserDataCommandProtocol[ExerciseProcessAction],
                ExerciseParameters,
                CaseMeta,
                HasRepositoryUserCommand[Filter, Updates],
            ],
        ],
        service_registry: dict[
            ExerciseProcessEnum,
            ServiceProtocol[
                HasRepositoryUserCommand[Filter, Updates],
                HasExerciseStatus,
            ],
        ],
    ) -> None:
        """Construct the use case."""
        self._store_prefix = store_prefix
        self._storage = storage
        self._adapter_registry = adapter_registry
        self._service_registry = service_registry

    @override
    def execute(
        self,
        command: UserDataCommandProtocol[ExerciseProcessAction],
    ) -> HasExerciseStatus:
        """Process exercise perform."""
        action = command.data['action']
        adapter = self._adapter_registry[action]
        service = self._service_registry[action]

        meta = self._storage.retrieve(command, self._store_prefix)  # type: ignore
        adapted = adapter.adapt(command, meta)  # type: ignore
        result = service.execute(adapted)  # type: ignore

        return result
