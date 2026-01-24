"""Language discipline presentation exercise UseCase."""

from typing import Any

from .. import schemas, types
from ..schemas import dto
from . import UseCase

type RequestData = dict[str, Any]

# ------------
# Presentation
# ------------


class ApiPresentationUseCase(
    UseCase[
        RequestData,
        schemas.PresentationRequest,
        dto.PresentationCase,
        types.TranslationAPI,
    ]
):
    """Api presentation UseCase."""


class WebPresentationUseCase(
    UseCase[
        RequestData,
        schemas.PresentationRequest,
        dto.PresentationCase,
        types.TranslationWEB,
    ]
):
    """Web presentation UseCase."""
