"""Response core adapters."""

__all__ = (
    # Null adapter
    'NullResponseAdapter',
    # Web adapters
    'PresentationTaskWebAdapter',
    # Adapter strategies
    'ProcessExerciseAdapterStrategy',
)

from .exercise.presentation.web import PresentationTaskWebAdapter
from .exercise.strategy import ProcessExerciseAdapterStrategy
from .null import NullResponseAdapter
