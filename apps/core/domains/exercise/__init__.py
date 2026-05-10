"""Core exercise domain."""

__all__ = (
    # Presentation exercise
    'PresentationDomain',
    # TEst exercise
    'TestDomain',
    'TestExerciseCheckDomain',
)

from .presentation import (
    PresentationDomain,
)
from .test import (
    TestDomain,
    TestExerciseCheckDomain,
)
