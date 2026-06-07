"""Entities."""


class ItemStudy:
    """Represents a single item to be studied."""

    def __init__(
        self,
        pk: int,
        define: str,
        explain: str,
    ) -> None:
        self._pk = pk
        self._define = define
        self._explain = explain

    @property
    def pk(self) -> int:
        """Get item identifier."""
        return self._pk

    @property
    def define(self) -> str:
        """Get item definition."""
        return self._define

    @property
    def explain(self) -> str:
        """Get item explanation."""
        return self._explain
