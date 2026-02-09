"""Language discipline services."""

__all__ = [
    'PresentationService',
    'ProgressService',
]

from apps.core.service.exercise.presentation import PresentationService

from .exercise.progress import ProgressService
