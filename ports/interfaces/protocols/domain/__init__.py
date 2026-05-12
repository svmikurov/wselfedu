"""Protocols for domain interfaces."""

__all__ = (
    # Exercise configuration
    'ExerciseConfigProtocol',
    # Exercise kind entity
    'PresentationTaskProtocol',
    'TestTaskProtocol',
    # Exercise domain attributes
    'TestAnswerProtocol',
    # Exercise domain result
    'PresentationDomainResultProtocol',
    'TestDomainResultProtocol',
    'CheckTestAnswerDomainResultProtocol',
)

from .exercise import (
    CheckTestAnswerDomainResultProtocol,
    ExerciseConfigProtocol,
    PresentationDomainResultProtocol,
    PresentationTaskProtocol,
    TestAnswerProtocol,
    TestDomainResultProtocol,
    TestTaskProtocol,
)
