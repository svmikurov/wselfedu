"""Auditor."""

import logging
from typing import Iterable, override

from .abstract import AbstractAuditor

log = logging.getLogger('audit')

HANDLER_STEPS: set[str] = {
    'handler.start',
    'validation.ok',
    'assembler.ok',
    'use_case.ok',
    'handler.finish',
}


class NullAuditor(AbstractAuditor):
    """Null auditor."""

    @override
    def record(self, step_name: str = '', **kwargs: object) -> None:
        """Record the attributes."""
        pass


class HandlerAuditor(AbstractAuditor):
    """Auditor."""

    MESSAGE = '[AUDIT] {} {}'

    def __init__(
        self,
        steps: Iterable[str] | None = None,
    ) -> None:
        """Construct the auditor."""
        self._steps = steps or HANDLER_STEPS

    @override
    def record(
        self,
        step_name: str,
        obj: object | None = None,
        **kwargs: object,
    ) -> None:
        """Record the attributes."""
        if step_name not in self._steps:
            return

        obj_repr = (
            f' | {type(obj).__module__}.{type(obj).__name__}' if obj else ''
        )

        details = [repr({k: v}) for k, v in kwargs.items()]

        if details:
            msg = f'{step_name}{obj_repr}\n{" | ".join(details)}'
            self._record(msg)

    @staticmethod
    def _record(message: str) -> None:
        log.debug(message)
