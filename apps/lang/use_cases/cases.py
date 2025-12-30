"""Language discipline UseCase."""

from typing import Any

from .. import schemas, types
from ..schemas import dto
from . import BaseUseCase

type RequestData = dict[str, Any]

# ------------
# Presentation
# ------------


class ApiPresentationUseCase(
    BaseUseCase[
        RequestData,
        schemas.PresentationRequest,
        dto.PresentationCase,
        types.TranslationAPI,
    ]
):
    """Api presentation UseCase."""


class WebPresentationUseCase(
    BaseUseCase[
        RequestData,
        schemas.PresentationRequest,
        dto.PresentationCase,
        types.TranslationWEB,
    ]
):
    """Web presentation UseCase."""


# ----
# Test
# ----


class WebTestUseCase(
    BaseUseCase[
        RequestData,
        schemas.TestRequestDTO,
        schemas.Case | schemas.Explanation,
        schemas.TestResponseData,
    ]
):
    """Web translation study test exercise UseCase."""
