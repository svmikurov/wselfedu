"""Auditable object's mixins."""

from functools import cached_property

from .impl import NullAuditor
from .protocol import Auditable, AuditorProtocol


class BaseAuditable(Auditable):
    """Base auditable."""

    def __init__(
        self,
        name: str | None = None,
        auditor: AuditorProtocol | None = None,
    ) -> None:
        """Construct the auditable."""
        self._name = name
        self._auditor = auditor

    @property
    def name(self) -> str:
        """Return request handler's name.

        Provides handler's name that given on handler initialization,
        for example, initialization in DI container.
        """
        return self._name  # type: ignore

    @cached_property
    def auditor(self) -> AuditorProtocol:
        """Return auditor."""
        return self._auditor or NullAuditor()
