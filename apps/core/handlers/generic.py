"""Generic request handler."""

from typing import Generic, TypeVar

from apps.core.adapters.response.protocol import AdapterProtocol
from apps.core.assemblers.protocol import AssemblerProtocol
from apps.core.use_cases.protocol import UseCaseProtocol
from apps.core.validators.request.protocol import RequestValidatorProtocol
from utils.audit.impl import NullAuditor
from utils.audit.protocol import AuditorProtocol
from utils.logger.decorators import log_errors_to_file

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
        validator: RequestValidatorProtocol[
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
        auditor: AuditorProtocol | None = None,
    ) -> None:
        """Construct the handler."""
        self._validator = validator
        self._assembler = assembler
        self._use_case = use_case
        self._adapter = adapter
        self._auditor = auditor or NullAuditor()

    @log_errors_to_file()
    def execute(
        self,
        params: RequestParams,
        context: RequestContext,
        data: RequestData,
    ) -> ResponseData:
        """Execute."""
        self._auditor.record(
            'handler.start',
            params=params,
            context=context,
            data=data,
        )

        validated = self._validator.validate(data)
        self._auditor.record(
            'validation.ok',
            obj=self._validator,
            validated=validated,
        )

        command = self._assembler.prepare(params, context, validated)
        self._auditor.record(
            'assembler.ok',
            obj=self._assembler,
            command=command,
        )

        domain_result = self._use_case.execute(command)
        self._auditor.record(
            'use_case.ok',
            obj=self._use_case,
            domain_result=domain_result,
        )

        adapted = self._adapter.to_response(domain_result, context)
        self._auditor.record(
            'handler.finish',
            obj=self._adapter,
            adapted=adapted,
        )

        return adapted
