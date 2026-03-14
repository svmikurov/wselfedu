"""Mathematical discipline handler types."""

from apps.core.adapters.response.shared import WebResponseDTO
from apps.core.handlers.dto import QueryParams, RequestContext, RequestData
from apps.core.handlers.generic import RequestHandler
from apps.core.handlers.protocol import RequestDataProtocol
from apps.core.parsers.request import NullParser
from apps.core.validators.request.null import NullValidator
from apps.math.domains.dto import StudentExerciseDTO

StudentExerciseListHandler = RequestHandler[
    QueryParams,
    RequestContext,
    RequestData,
    NullParser,
    NullValidator[RequestDataProtocol],
    list[StudentExerciseDTO],
    WebResponseDTO,
]
