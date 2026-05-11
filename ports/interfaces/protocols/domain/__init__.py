"""Protocols for domain interfaces."""

__all__ = (
    'PresentationDomainResultProtocol',
    'CheckTestAnswerDomainResultProtocol',
)

from .exercise import (
    CheckTestAnswerDomainResultProtocol,
    PresentationDomainResultProtocol,
)
