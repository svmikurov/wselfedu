"""Generic request handler."""

from typing import Generic, TypeVar

from .protocol import (
    AdapterProtocol,
    QueryRequestParamsProtocol,
    RequestParserProtocol,
    UseCaseProtocol,
    ValidatorProtocol,
)

RequestParams = TypeVar('RequestParams', bound=QueryRequestParamsProtocol)
RequestContext = TypeVar('RequestContext')
RequestData = TypeVar('RequestData')
Parsed = TypeVar('Parsed')
Validated = TypeVar('Validated')
DomainResult = TypeVar('DomainResult')
ResponseData = TypeVar('ResponseData')


class RequestHandler(
    Generic[
        RequestParams,
        RequestContext,
        RequestData,
        Parsed,
        Validated,
        DomainResult,
        ResponseData,
    ]
):
    """Generic request handler."""

    def __init__(
        self,
        parser: RequestParserProtocol[Parsed,],
        validator: ValidatorProtocol[
            RequestData,
            Validated,
        ],
        use_case: UseCaseProtocol[
            Parsed,
            RequestContext,
            Validated,
            DomainResult,
        ],
        adapter: AdapterProtocol[
            DomainResult,
            RequestContext,
            ResponseData,
        ],
    ) -> None:
        """Construct the handler."""
        self._parser = parser
        self._validator = validator
        self._use_case = use_case
        self._adapter = adapter

    def execute(
        self,
        params: RequestParams,
        context: RequestContext,
        data: RequestData,
    ) -> ResponseData:
        """Execute."""
        parsed = self._parser.parse(params)
        validated = self._validator.validate(data)
        domain_result = self._use_case.execute(parsed, context, validated)
        result = self._adapter.to_response(domain_result, context)
        return result
