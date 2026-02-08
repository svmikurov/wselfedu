"""Exercise request handler types."""

from typing import Any

from apps.core import handlers
from apps.lang import schemas
from apps.lang.schemas.dto import PresentationCase
from apps.lang.types import TranslationAPI

type RequestData = dict[str, Any]

type RegularPresentationApiHandler = handlers.RegularRequestHandler[
    RequestData,
    schemas.RegularConditionRequest,
    PresentationCase,
    TranslationAPI,
]
