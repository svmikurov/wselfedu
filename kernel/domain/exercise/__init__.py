"""Exercise domain."""

__all__ = (
    # Prepare exercise
    'CandidatesSelector',
    # Presentation exercise
    'PresentationDomain',
    # Test exercise
    'TestDomain',
    'TestExerciseCheckDomain',
    'ExplainTestAnswerDomain',
)

from .presentation import PresentationDomain
from .selector import CandidatesSelector
from .test import ExplainTestAnswerDomain, TestDomain, TestExerciseCheckDomain
