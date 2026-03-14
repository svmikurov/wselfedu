"""Handler type hint."""

from typing import TypeAlias

from apps.core.handlers.dto import QueryParams, RequestContext, RequestData
from apps.core.handlers.protocol import RequestDataProtocol
from apps.core.parsers.request import NullParser
from apps.core.validators.request.null import NullValidator

# TODO: Relocate schemas
from apps.lang.schemas import (
    DetailTestRequestDTO,
    TestResponseData,
)

from .generic import RequestHandler

WebTest: TypeAlias = RequestHandler[
    QueryParams,
    RequestContext,
    RequestData,
    NullParser,
    NullValidator[RequestDataProtocol],
    DetailTestRequestDTO,
    TestResponseData,
]
"""Regular web translation study test exercise use case."""

WebAssignedTest: TypeAlias = RequestHandler[
    QueryParams,
    RequestContext,
    RequestData,
    NullParser,
    NullValidator[RequestDataProtocol],
    DetailTestRequestDTO,
    TestResponseData,
]
"""Detail web translation study test exercise use case."""
