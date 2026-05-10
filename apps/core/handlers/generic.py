"""Generic request handler."""

from typing import Generic, TypeVar

from apps.core.assemblers.protocol import AuditableAssemblerProtocol
from apps.core.use_cases.protocol import UseCaseProtocol
from apps.core.validators.request.protocol import RequestValidatorProtocol
from ports.contract.infra.adapter import AdapterProtocol
from utils.audit.base import BaseAuditable
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
    BaseAuditable,
    Generic[
        RequestParams,
        RequestContext,
        RequestData,
        Validated,
        CommandData,
        DomainResult,
        ResponseData,
    ],
):
    """Generic request handler."""

    def __init__(
        self,
        validator: RequestValidatorProtocol[
            RequestData,
            Validated,
        ],
        assembler: AuditableAssemblerProtocol[
            RequestParams,
            RequestContext,
            Validated,
            CommandData,
        ],
        use_case: UseCaseProtocol[CommandData, DomainResult],
        adapter: AdapterProtocol[DomainResult, RequestContext, ResponseData],
        name: str | None = None,
        auditor: AuditorProtocol | None = None,
    ) -> None:
        """Construct the handler."""
        super().__init__(name=name, auditor=auditor)
        self._validator = validator
        self._assembler = assembler
        self._use_case = use_case
        self._adapter = adapter

    @log_errors_to_file()
    def execute(
        self,
        params: RequestParams,
        context: RequestContext,
        data: RequestData,
    ) -> ResponseData:
        """Execute."""
        self.auditor.record(
            'handler.start',
            obj=self,
            params=params,
            context=context,
            data=data,
        )

        self.auditor.record('validator.call', obj=self._validator)
        validated = self._validator.validate(data)
        self.auditor.record('validator.ok', validated=validated)

        self.auditor.record('assembler.call', obj=self._assembler)
        command = self._assembler.prepare(params, context, validated)
        self.auditor.record('assembler.ok', command=command)

        self.auditor.record('use_case.call', obj=self._use_case)
        domain_result = self._use_case.execute(command)
        self.auditor.record('use_case.ok', domain_result=domain_result)

        self.auditor.record('adapter.call', obj=self._adapter)
        adapted = self._adapter.to_response(domain_result, context)
        self.auditor.record('adapter.ok', adapted=adapted)

        self.auditor.record('handler.finish')
        return adapted
