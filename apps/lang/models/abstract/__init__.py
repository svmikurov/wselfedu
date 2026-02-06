"""Language discipline abstract models."""

__all__ = [
    'AbstractWordModel',
    'AbstractProgressModel',
]

from .progress import AbstractProgressModel
from .word import AbstractWordModel
