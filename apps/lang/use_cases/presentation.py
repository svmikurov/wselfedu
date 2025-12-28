"""Get presentation UseCase."""

from __future__ import annotations

from typing import Any

from .. import schemas, types
from ..schemas import dto
from .base import BaseUseCase


class ApiPresentationUseCase(
    BaseUseCase[
        dict[str, Any],
        schemas.PresentationRequest,
        dto.PresentationCase,
        types.TranslationAPI,
    ]
):
    """Api presentation UseCase."""


class WebPresentationUseCase(
    BaseUseCase[
        dict[str, Any],
        schemas.PresentationRequest,
        dto.PresentationCase,
        types.TranslationWEB,
    ]
):
    """Web presentation UseCase."""
