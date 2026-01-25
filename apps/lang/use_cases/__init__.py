"""Language discipline UseCase."""

__all__ = [
    # Base
    'UseCase',
    'DetailUseCase',
    # Presentation
    'ApiPresentationUseCase',
    'WebPresentationUseCase',
]

from .generic import DetailUseCase, UseCase
from .presentation import (
    ApiPresentationUseCase,
    WebPresentationUseCase,
)
