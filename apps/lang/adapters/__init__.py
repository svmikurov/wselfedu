"""Language discipline API & WEB response adapters."""

__all__ = [
    'WebTestExerciseAdapter',
    'WebRuleAdapter',
]

from ...core.adapters.response.exercise.test.web import WebTestExerciseAdapter
from .response.rule import WebRuleAdapter
