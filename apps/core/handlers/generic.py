"""Generic request handler."""

from typing import Generic, TypeVar

from apps.core.assemblers.protocol import AssemblerProtocol
from apps.core.use_cases.protocol import UseCaseProtocol

from .protocol import (
    AdapterProtocol,
    ValidatorProtocol,
)

# External data
RequestParams = TypeVar('RequestParams')
RequestContext = TypeVar('RequestContext')
RequestData = TypeVar('RequestData')

# Internal data
Validated = TypeVar('Validated')
CommandData = TypeVar('CommandData')

# Result data
DomainResult = TypeVar('DomainResult')
ResponseData = TypeVar('ResponseData')


class RequestHandler(
    Generic[
        RequestParams,
        RequestContext,
        RequestData,
        Validated,
        CommandData,
        DomainResult,
        ResponseData,
    ]
):
    """Generic request handler."""

    def __init__(
        self,
        validator: ValidatorProtocol[
            RequestData,
            Validated,
        ],
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
        data: RequestData,
    ) -> ResponseData:
        """Execute."""
        validated = self._validator.validate(data)
        command = self._assembler.prepare(params, context, validated)
        domain_result = self._use_case.execute(command)
        adapted = self._adapter.to_response(domain_result, context)
        return adapted
