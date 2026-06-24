"""Request handlers."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from .dtos import ResponseDto

if TYPE_CHECKING:
    from .protocols import HasContext, SimpleRequestParamsProto

ContextT = TypeVar('ContextT')
DataT = TypeVar('DataT')


class ExerciseHandler:
    """Exercise performing request handler."""

    def execute(
        self,
        params: SimpleRequestParamsProto[ContextT, DataT],
    ) -> HasContext[dict[str, str]]:
        """Execute the exercise request."""
        return ResponseDto(context={'no_key': 'no_value'})
