"""Abstract base class http entrypoint layer."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, override

from ..interfaces.protocols import Preparable, ResponseAdaptable, Validatable

RequestParamsT = TypeVar('RequestParamsT')
RequestContextT = TypeVar('RequestContextT')
RequestDataT = TypeVar('RequestDataT')

ValidatedT = TypeVar('ValidatedT')
CommandT = TypeVar('CommandT')
ResultT = TypeVar('ResultT')
AdaptedT = TypeVar('AdaptedT')


class AbstractValidator(ABC, Validatable[RequestDataT, ValidatedT]):
    """ABC for validator."""

    @override
    @abstractmethod
    def validate(self, data: RequestDataT) -> ValidatedT:
        """Validate."""


class AbstractAssembler(
    ABC, Preparable[RequestParamsT, RequestContextT, RequestDataT, CommandT]
):
    """ABC for assembler."""

    @override
    @abstractmethod
    def prepare(
        self,
        params: RequestParamsT,
        context: RequestContextT,
        validated: RequestDataT,
    ) -> CommandT:
        """Prepare command."""


class AbstractAdapter(
    ABC, ResponseAdaptable[ResultT, RequestContextT, AdaptedT]
):
    """ABC for response adapter."""

    @override
    @abstractmethod
    def to_response(
        self, source: ResultT, context: RequestContextT
    ) -> AdaptedT:
        """Adapt source for response context."""


class AbstractRequestHandler(
    ABC, Generic[RequestParamsT, RequestContextT, RequestDataT, ResultT]
):
    """ABC for request handler."""

    @abstractmethod
    def handle(
        self,
        params: RequestParamsT,
        context: RequestContextT,
        data: RequestDataT,
    ) -> ResultT:
        """Handle the request."""
