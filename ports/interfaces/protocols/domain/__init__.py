"""Protocols for domain interfaces."""

__all__ = (
    'PresentationDomainResultProtocol',
    'CheckTestAnswerDomainResultProtocol',
    'TestDomainResultProtocol',
    'TestTaskProtocol',
    'ExerciseConfigProtocol',
)

from .exercise import (
    CheckTestAnswerDomainResultProtocol,
    ExerciseConfigProtocol,
    PresentationDomainResultProtocol,
    TestDomainResultProtocol,
    TestTaskProtocol,
)
