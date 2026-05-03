"""Repository with use case interface."""

from typing import TypeVar

from apps.core.builders.abstract import AbstractLockupConditionsFactory
from apps.core.repositories.protocol import RepositoryProtocol
from apps.core.use_cases.abstract import AbstractUseCase

LockupCommandT = TypeVar('LockupCommandT')
LockupConditionsT = TypeVar('LockupConditionsT')
QueryResultT = TypeVar('QueryResultT')


class RepositoryUseCase(AbstractUseCase[LockupCommandT, QueryResultT]):
    """Repository with use case interface."""

    def __init__(
        self,
        lockup_factory: AbstractLockupConditionsFactory[
            LockupCommandT,
            LockupConditionsT,
        ],
        repository: RepositoryProtocol[LockupConditionsT, QueryResultT],
    ) -> None:
        """Construct the repository."""
        self._lockup_factory = lockup_factory
        self._repository = repository

    def execute(self, command: LockupCommandT) -> QueryResultT:
        """Return query result."""
        lockup_conditions = self._lockup_factory.build(command)
        return self._repository.fetch(lockup_conditions)  # type: ignore
