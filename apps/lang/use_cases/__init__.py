"""Language discipline UseCase."""

__all__ = [
    # Base
    'UseCase',
    'DetailUseCase',
    # Presentation
    'ApiPresentationUseCase',
    'WebPresentationUseCase',
    # Test exercise
    'WebTestUseCase',
    'AssignmentUseCase',
]

from .base import DetailUseCase, UseCase
from .presentation import (
    ApiPresentationUseCase,
    WebPresentationUseCase,
)
from .test import (
    AssignmentUseCase,
    WebTestUseCase,
)
