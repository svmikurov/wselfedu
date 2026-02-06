"""Language discipline API & WEB response adapters."""

# REVIEW: Package export, export organization.

__all__ = [
    # Presentation exercise
    'WebPresentationAdapter',
    'ApiPresentationAdapter',
    # Test exercise
    'WebTestAdapter',
    # Rule content
    'WebRuleAdapter',
]

from .response.exercise.presentation import ApiPresentationAdapter
from .response.exercise.test import WebTestAdapter
from .response.rule import WebRuleAdapter
from .web_presentation import WebPresentationAdapter
