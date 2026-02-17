"""Abstract base classes for use cases."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from apps.core.handlers.protocol import (
        DetailParamsProtocol,
        RequestContextProtocol,
    )
    from apps.users.models import Person

ResponseData = TypeVar('ResponseData')
RequestData = TypeVar('RequestData')


class AbstractUseCase(ABC, Generic[RequestData, ResponseData]):
    """ABC for use case."""

    @abstractmethod
    def execute(self, user: Person, request_data: RequestData) -> ResponseData:
        """Execute use case."""


class AbstractDetailUseCase(ABC, Generic[ResponseData]):
    """ABC for detail use case."""

    @abstractmethod
    def execute(
        self,
        params: DetailParamsProtocol,
        context: RequestContextProtocol,
        data: object,
    ) -> ResponseData:
        """Execute use case."""
