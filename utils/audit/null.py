"""Auditor."""

from typing import override

from .abstract import AbstractAuditor
from .protocol import Auditable


class NullAuditor(AbstractAuditor):
    """Null auditor."""

    @override
    def record(
        self,
        step_name: str,
        obj: Auditable | None = None,
        **kwargs: object,
    ) -> None:
        """Record the attributes."""
        pass
