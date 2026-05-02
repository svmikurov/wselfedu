"""Auditor."""

import inspect
import logging
import uuid
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
        parent_id: str | None = None,
        obj: Auditable | None = None,
        **kwargs: object,
    ) -> None:
        """Record the attributes."""
        pass


# TODO: Update auditor
# Implement single schema for string and json representation
class Auditor(AbstractAuditor):
    """Auditor."""

    def __init__(self) -> None:
        """Construct the auditor."""
        self._auditor_id = str(uuid.uuid4())[:8]

    @override
    def record(
        self,
        step_name: str,
        parent_id: str | None = None,
        obj: Auditable | None = None,
        **kwargs: object,
    ) -> None:
        """Record the attributes."""
        class_name = f'class name: {type(obj).__name__}'
        message_parts = [class_name]

        obj_name = ''
        if obj and obj.name and obj.name != 'undefined':
            obj_name = f' {obj.name}'

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

        msg = f'[{self._auditor_id}] {step_name}{obj_name}'
        if obj_repr:
            msg += f'\n{obj_repr}'
        if details_repr:
            msg += details_repr

        self._record(msg)

    @staticmethod
    def _record(message: str) -> None:
        log.debug(message)
