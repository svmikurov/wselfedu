"""Abstract base classes for use cases."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, override

from apps.core.handlers.protocol import UseCaseProtocol

__all__ = ('AbstractUseCase',)

RequestParams = TypeVar('RequestParams')
RequestContext = TypeVar('RequestContext')
Validated = TypeVar('Validated')
ResultData = TypeVar('ResultData')


class AbstractUseCase(
    ABC,
    UseCaseProtocol[
        RequestParams,
        RequestContext,
        Validated,
        ResultData,
    ],
):
    """ABC for generic request use case."""

    @override
    @abstractmethod
    def execute(
        self,
        params: RequestParams,
        context: RequestContext,
        validated: Validated,
    ) -> ResultData:
        """Execute use case."""
