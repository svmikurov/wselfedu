"""Generic request handler."""

from typing import Any, Generic, TypeVar

from apps.core.assemblers.protocol import AssemblerProtocol

from .protocol import (
    AdapterProtocol,
    UseCaseProtocol,
    ValidatorProtocol,
)

# Request data
RequestParams = TypeVar('RequestParams')
RequestContext = TypeVar('RequestContext')
Validated = TypeVar('Validated')
CommandData = TypeVar('CommandData')

# Result data
DomainResult = TypeVar('DomainResult')
ResponseData = TypeVar('ResponseData')


class RequestHandler(
    Generic[
        RequestParams,
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
        assembler: AssemblerProtocol[
            RequestParams,
            RequestContext,
            Validated,
            CommandData,
        ],
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
        params: RequestParams,
        context: RequestContext,
        data: dict[str, Any],
    ) -> ResponseData:
        """Execute."""
        validated = self._validator.validate(data)
        command = self._assembler.prepare(params, context, validated)
        domain_result = self._use_case.execute(command)
        return self._adapter.to_response(domain_result, context)
