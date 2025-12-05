"""Language app domain logic."""

__all__ = [
    # ABC
    'WordStudyDomainABC',
    # Implementation
    'WordStudyDomain',
]

from .abc import WordStudyDomainABC
from .presentation import WordStudyDomain
