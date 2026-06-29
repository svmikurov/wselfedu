"""Request handler."""

from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar, override

from .abstract import AbstractRequestHandler

if TYPE_CHECKING:
    from wse.application.protocols import Executable

    from .protocols import Preparable, ResponseAdaptable, Validatable

RequestParamsT = TypeVar('RequestParamsT')
RequestContextT = TypeVar('RequestContextT')
RequestDataT = TypeVar('RequestDataT')

ValidatedT = TypeVar('ValidatedT')
CommandT = TypeVar('CommandT')
ResultT = TypeVar('ResultT')
AdaptedT = TypeVar('AdaptedT')


class RequestHandler(
    AbstractRequestHandler[
        RequestParamsT,
        RequestContextT,
        RequestDataT,
        AdaptedT,
    ],
    Generic[
        RequestParamsT,
        RequestContextT,
        RequestDataT,
        ValidatedT,
        CommandT,
        ResultT,
        AdaptedT,
    ],
):
    """Request handler."""

    def __init__(
        self,
        validator: Validatable[RequestDataT, ValidatedT],
        assembler: Preparable[
            RequestParamsT,
            RequestContextT,
            ValidatedT,
            CommandT,
        ],
        use_case: Executable[CommandT, ResultT],
        adapter: ResponseAdaptable[ResultT, RequestContextT, AdaptedT],
    ) -> None:
        self._assembler = assembler
        self._validator = validator
        self._use_case = use_case
        self._adapter = adapter

    @override
    def handle(
        self,
        params: RequestParamsT,
        context: RequestContextT,
        data: RequestDataT,
    ) -> AdaptedT:
        """Handle a request."""
        validated = self._validator.validate(data)
        command = self._assembler.prepare(params, context, validated)
        result = self._use_case.execute(command)
        adapted = self._adapter.to_response(result, context)
        return adapted
