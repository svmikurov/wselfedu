"""Response core adapters."""

__all__ = (
    # Web adapters
    'PresentationTaskWebAdapter',
    # Adapter strategies
    'ProcessExerciseAdapterStrategy',
)

from .exercise.presentation.web import PresentationTaskWebAdapter
from .exercise.strategy import ProcessExerciseAdapterStrategy
