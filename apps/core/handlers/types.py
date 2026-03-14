"""Handler type hint."""

from typing import Any, TypeAlias

from apps.core.handlers.dto import QueryParams, RequestContext
from apps.core.parsers.request import NullParser

# TODO: Relocate schemas
from apps.lang import schemas

from .generic import RequestHandler

type RequestData = dict[str, Any]
type DomainResult = schemas.TestCase | schemas.Explanation


WebTest: TypeAlias = RequestHandler[
    QueryParams,
    RequestContext,
    RequestData,
    NullParser,
    schemas.TestRequestDTO,
    DomainResult,
    schemas.TestResponseData,
]
"""UseCase for regular web translation study tests."""

WebAssignedTest: TypeAlias = RequestHandler[
    QueryParams,
    RequestContext,
    RequestData,
    NullParser,
    schemas.DetailTestRequestDTO,
    DomainResult,
    schemas.TestResponseData,
]
"""UseCase for web translation tests with assignment pk."""
