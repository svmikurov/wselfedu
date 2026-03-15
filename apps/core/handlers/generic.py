"""Generic request handler."""

from typing import Any, Generic, TypeVar

from .protocol import (
    AdapterProtocol,
    AssemblerProtocol,
    UseCaseProtocol,
    ValidatorProtocol,
)

# Request data
RequestContext = TypeVar('RequestContext')
Validated = TypeVar('Validated')
CommandData = TypeVar('CommandData')

# Result data
DomainResult = TypeVar('DomainResult')
ResponseData = TypeVar('ResponseData')


class RequestHandler(
    Generic[
        RequestContext,
        Validated,
        CommandData,
        DomainResult,
        ResponseData,
    ]
):
    """Generic request handler."""

    def __init__(
        self,
        validator: ValidatorProtocol[Validated],
        assembler: AssemblerProtocol[RequestContext, Validated, CommandData],
        use_case: UseCaseProtocol[CommandData, DomainResult],
        adapter: AdapterProtocol[DomainResult, RequestContext, ResponseData],
    ) -> None:
        """Construct the handler."""
        self._validator = validator
        self._assembler = assembler
        self._use_case = use_case
        self._adapter = adapter

    def execute(
        self,
        params: dict[str, str],
        context: RequestContext,
        data: dict[str, Any],
    ) -> ResponseData:
        """Execute."""
        validated = self._validator.validate(data)
        command = self._assembler.prepare(params, context, validated)
        domain_result = self._use_case.execute(command)
        return self._adapter.to_response(domain_result, context)
