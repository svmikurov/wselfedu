"""Domain entities."""


class StudyItem:
    """Item for study."""

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
        """Provide item identifier."""
        return self._pk

    @property
    def define(self) -> str:
        """Provide item definition."""
        return self._define

    @property
    def explain(self) -> str:
        """Provide item explanation."""
        return self._explain
