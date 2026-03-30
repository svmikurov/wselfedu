"""Simple use case."""

from typing import TypeVar

from apps.core.factories.abstract import AbstractLockupConditionsFactory
from apps.core.repositories.protocol import UserRepositoryProtocol
from apps.core.use_cases.abstract import AbstractUseCase

LockupCommand = TypeVar('LockupCommand')
LockupConditions = TypeVar('LockupConditions')
QueryResult = TypeVar('QueryResult')


class RepositoryUseCase(AbstractUseCase[LockupCommand, QueryResult]):
    """Request with lockup conditions the use case."""

    def __init__(
        self,
        lockup_factory: AbstractLockupConditionsFactory[
            LockupCommand,
            LockupConditions,
        ],
        repository: UserRepositoryProtocol[LockupConditions, QueryResult],
    ) -> None:
        """Construct the use case."""
        self._lockup_factory = lockup_factory
        self._repository = repository

    def execute(self, command: LockupCommand) -> QueryResult:
        """Return query result."""
        lockup_conditions = self._lockup_factory.build(command)
        return self._repository.fetch(lockup_conditions)
