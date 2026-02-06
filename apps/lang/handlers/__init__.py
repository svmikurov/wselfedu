"""Language discipline UseCase."""

__all__ = [
    # Base
    'RegularRequestHandler',
    'DetailRequestHandler',
    # Presentation
    'ApiPresentationUseCase',
    'WebPresentationUseCase',
]

from ...core.handlers.generic import (
    DetailRequestHandler,
    RegularRequestHandler,
)
from .presentation import (
    ApiPresentationUseCase,
    WebPresentationUseCase,
)
