"""Language discipline request handler type."""

from typing import Any, TypeAlias

from apps.core.domains.exercise.dto import TestResponseData
from apps.core.domains.exercise.test import Result
from apps.core.handlers.dto import QueryParams, RequestContext, RequestData
from apps.core.handlers.generic import RequestHandler
from apps.core.handlers.protocol import RequestDataProtocol
from apps.core.parsers.request import NullParser
from apps.core.validators.request.null import NullValidator

RegularTranslationTestWebHandler: TypeAlias = RequestHandler[
    QueryParams,
    RequestContext,
    RequestData,
    NullParser,
    NullValidator[RequestDataProtocol],
    Result,
    TestResponseData,
]

RegularPresentationApiHandler: TypeAlias = Any
