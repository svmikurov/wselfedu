"""Handler type hint."""

from typing import Any, TypeAlias

# TODO: Relocate schemas
from ...lang import schemas
from .generic import RegularRequestHandler, ResourceRequestHandler

type RequestData = dict[str, Any]
type DomainResult = schemas.TestCase | schemas.Explanation


WebTest: TypeAlias = RegularRequestHandler[
    RequestData,
    schemas.TestRequestDTO,
    DomainResult,
    schemas.TestResponseData,
]
"""UseCase for regular web translation study tests."""

WebAssignedTest: TypeAlias = ResourceRequestHandler[
    RequestData,
    schemas.DetailTestRequestDTO,
    DomainResult,
    schemas.TestResponseData,
]
"""UseCase for web translation tests with assignment pk."""
