"""Use case strategy."""

import logging
from typing import Generic, TypeVar, override

from apps.core.assemblers.protocol import DataCommandProtocol
from apps.core.use_cases.protocol import UseCaseProtocol
from interfaces.protocols.domain.general import HasAction

from .abstract import AbstractUseCase

ActionT = TypeVar('ActionT')
ResultT = TypeVar('ResultT')

log = logging.getLogger(__name__)

# NOTE: Unused use case strategy


class UseCaseStrategy(
    AbstractUseCase[DataCommandProtocol[HasAction[ActionT]], ResultT],
    Generic[ActionT, ResultT],
):
    """Use case strategy."""

    def __init__(
        self,
        registry: dict[
            ActionT,
            UseCaseProtocol[DataCommandProtocol[HasAction[ActionT]], ResultT],
        ],
    ) -> None:
        """Construct the strategy."""
        self._registry = registry

    @override
    def execute(
        self,
        command: DataCommandProtocol[HasAction[ActionT]],
    ) -> ResultT:
        """Execute."""
        action = command.data.action

        try:
            return self._registry[action].execute(command)
        except KeyError:
            log.error(f'No registered use case for "{action}" strategy key')
            raise
