"""Core exercise domain."""

__all__ = (
    'PresentationDomain',
    'TestExerciseCheckDomain',
)

from .presentation.impl import (
    PresentationDomain,
)
from .test.impl import (
    TestExerciseCheckDomain,
)
