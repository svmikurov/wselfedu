"""Abstract base class for assembler."""

from abc import ABC, abstractmethod
from typing import TypeVar, override

from ports.contract.entity.command import AssemblerProtocol

RequestParams = TypeVar('RequestParams')
RequestContext = TypeVar('RequestContext')
Validated = TypeVar('Validated')
CommandData = TypeVar('CommandData')


class AbstractAssembler(
    ABC,
    AssemblerProtocol[RequestParams, RequestContext, Validated, CommandData],
):
    """ABC for assembler."""

    @override
    @abstractmethod
    def prepare(
        self,
        params: RequestParams,
        context: RequestContext,
        data: Validated,
    ) -> CommandData:
        """Prepare request data for use case execute."""
