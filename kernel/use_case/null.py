"""Null use case."""

from ports.abstract.use_case import AbstractUseCase


class NullUseCase(AbstractUseCase[object, object]):
    """Null use case."""

    def execute(self, command: object) -> object:
        """Return command."""
        return command
