"""Language discipline API & WEB response adapters."""

__all__ = [
    'WebTestAdapter',
    'WebRuleAdapter',
]

from ...core.adapters.response.exercise.test.web import WebTestAdapter
from .response.rule import WebRuleAdapter
