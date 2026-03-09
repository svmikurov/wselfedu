"""Abstract base classes for resolvers."""

from abc import ABC, abstractmethod
from typing import override

from .protocol import (
    CompletionResolverProtocol,
    CompletionStateDataType,
    SuccessCountDataType,
)


class AbstractCompletionResolver(ABC, CompletionResolverProtocol):
    """ABC for exercise completion resolver."""

    @override
    @abstractmethod
    def get_completion_state(self, exercise: CompletionStateDataType) -> bool:
        """Resolve exercise completion state."""

    @override
    @abstractmethod
    def get_success_count(self, exercise: SuccessCountDataType) -> int:
        """Resolve exercise perform success count."""
