"""Null use case."""

from apps.core.use_cases.abstract import AbstractUseCase


class NullUseCase(AbstractUseCase[object, object]):
    """Null use case."""

    def execute(self, command: object) -> object:
        """Return command."""
        return command
