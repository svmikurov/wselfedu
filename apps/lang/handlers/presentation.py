"""Language discipline presentation exercise UseCase."""

from typing import Any

from .. import schemas, types
from ..schemas import dto
from . import RegularRequestHandler

type RequestData = dict[str, Any]

# ------------
# Presentation
# ------------

# DEPRECATED: Delete


class ApiPresentationUseCase(
    RegularRequestHandler[
        RequestData,
        schemas.RegularConditionRequest,
        dto.PresentationCase,
        types.TranslationAPI,
    ]
):
    """Api presentation UseCase."""


class WebPresentationUseCase(
    RegularRequestHandler[
        RequestData,
        schemas.RegularConditionRequest,
        dto.PresentationCase,
        types.TranslationWEB,
    ]
):
    """Web presentation UseCase."""
