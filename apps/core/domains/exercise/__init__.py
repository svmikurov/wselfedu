"""Core exercise domain."""

__all__ = (
    # Presentation exercise
    'PresentationDomain',
    # TEst exercise
    'TestDomain',
    'TestExerciseCheckDomain',
)

from .presentation.impl import (
    PresentationDomain,
)
from .test.impl import (
    TestDomain,
    TestExerciseCheckDomain,
)
