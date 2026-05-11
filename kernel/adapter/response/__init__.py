"""Response core adapters."""

__all__ = (
    # Web adapters
    'CreatePresentationWebAdapter',
    # Adapter strategies
    'ProcessExerciseAdapterStrategy',
)

from .exercise.presentation.web import CreatePresentationWebAdapter
from .exercise.strategy import ProcessExerciseAdapterStrategy
