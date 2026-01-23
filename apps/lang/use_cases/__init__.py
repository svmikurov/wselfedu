"""Language discipline UseCase."""

__all__ = [
    # Base
    'BaseUseCase',
    # Presentation
    'ApiPresentationUseCase',
    'WebPresentationUseCase',
    # Test exercise
    'WebTestUseCase',
    'AssignmentUseCase',
]

from .base import BaseUseCase
from .presentation import (
    ApiPresentationUseCase,
    WebPresentationUseCase,
)
from .test import (
    AssignmentUseCase,
    WebTestUseCase,
)
