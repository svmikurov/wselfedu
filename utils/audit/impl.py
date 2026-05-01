"""Auditor."""

import inspect
import logging
from typing import TypeVar, override

from .abstract import AbstractAuditor
from .protocol import Auditable

log = logging.getLogger('audit')

ObjectT = TypeVar('ObjectT', bound=Auditable)


# REFACTOR: Remove this null auditor definition
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


class Auditor(AbstractAuditor):
    """Auditor."""

    @override
    def record(
        self,
        step_name: str,
        obj: Auditable | None = None,
        **kwargs: object,
    ) -> None:
        """Record the attributes."""
        class_name = f'class name: {type(obj).__name__}'
        message_parts = [class_name]

        obj_name = ''
        if obj and obj.name and obj.name != 'undefined':
            obj_name = f'instance name: {obj.name!r}'
            message_parts.append(obj_name)

        obj_file_path = ''
        if obj:
            line = inspect.getsourcelines((type(obj)))[1]
            obj_file_path = (
                f'definition path: {inspect.getfile(type(obj))!r}, line {line}'
            )
            message_parts.append(obj_file_path)

        obj_repr = ' | '.join(message_parts) if obj else ''

        details = [repr({k: v}) for k, v in kwargs.items()]
        details_repr = '\n' + '\n'.join(details) if details else ''

        msg = f'{step_name}\n{obj_repr}{details_repr}'
        self._record(msg)

    @staticmethod
    def _record(message: str) -> None:
        log.debug(message)
