"""Handler type hint."""

from typing import TypeAlias

from apps.core.assemblers.protocol import (
    QueryCommandProtocol,
    UserDetailCommandProtocol,
)
from apps.core.handlers.dto import (
    QueryRequestParamsDTO,
    RequestContextDTO,
    RequestData,
)
from apps.core.handlers.protocol import RequestDataProtocol
from apps.core.validators.request.null import NullValidator

# TODO: Relocate schemas
from apps.lang.schemas import (
    DetailTestRequestDTO,
    TestResponseData,
)

from ..generic import RequestHandler

WebTest: TypeAlias = RequestHandler[
    QueryRequestParamsDTO,
    RequestContextDTO,
    RequestData,
    QueryCommandProtocol,
    NullValidator[RequestDataProtocol],
    DetailTestRequestDTO,
]
"""Regular web translation study test exercise use case."""

WebAssignedTest: TypeAlias = RequestHandler[
    QueryRequestParamsDTO,
    RequestContextDTO,
    RequestData,
    UserDetailCommandProtocol,
    NullValidator[RequestDataProtocol],
    TestResponseData,
]
"""Detail web translation study test exercise use case."""
