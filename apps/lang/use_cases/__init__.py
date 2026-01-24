"""Language discipline UseCase."""

__all__ = [
    # Base
    'UseCase',
    # Presentation
    'ApiPresentationUseCase',
    'WebPresentationUseCase',
    # Test exercise
    'WebTestUseCase',
    'AssignmentUseCase',
]

from .base import UseCase
from .presentation import (
    ApiPresentationUseCase,
    WebPresentationUseCase,
)
from .test import (
    AssignmentUseCase,
    WebTestUseCase,
)
