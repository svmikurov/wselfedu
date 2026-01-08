"""Language discipline API & WEB response adapters."""

# REVIEW: Package export, export organization.

__all__ = [
    # Base
    'WebRuleAdapterABC',
    # Presentation
    'WebPresentationAdapter',
    'ApiPresentationAdapter',
    # Test
    'WebTestAdapter',
    # Rule
    'WebRuleAdapter',
    # DTO
    'RuleSchema',
]

from .api_presentation import ApiPresentationAdapter
from .base import WebRuleAdapterABC
from .dto import RuleSchema
from .rule import WebRuleAdapter
from .test import WebTestAdapter
from .web_presentation import WebPresentationAdapter
